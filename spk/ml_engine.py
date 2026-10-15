import os
import json
import logging
from datetime import datetime
from pathlib import Path
from django.conf import settings

logger = logging.getLogger(__name__)

FEATURE_NAMES = [
    'nilai_matematika',
    'nilai_bahasa_indonesia',
    'nilai_bahasa_inggris',
    'nilai_ipa',
    'nilai_ips',
    'nilai_agama',
    'minat_teknologi',
    'minat_sains',
    'minat_bisnis',
    'minat_sosial',
    'minat_seni',
    'minat_pendidikan'
]

FEATURE_LABELS = {
    'nilai_matematika': 'Matematika',
    'nilai_bahasa_indonesia': 'Bahasa Indonesia',
    'nilai_bahasa_inggris': 'Bahasa Inggris',
    'nilai_ipa': 'IPA (Fisika/Biologi/Kimia)',
    'nilai_ips': 'IPS (Ekonomi/Geografi/Sosiologi)',
    'nilai_agama': 'Pendidikan Agama Islam',
    'minat_teknologi': 'Minat Teknologi & Komputer',
    'minat_sains': 'Minat Sains & Medis',
    'minat_bisnis': 'Minat Ekonomi & Bisnis',
    'minat_sosial': 'Minat Sosial & Hukum',
    'minat_seni': 'Minat Seni & Desain',
    'minat_pendidikan': 'Minat Pendidikan & Bahasa'
}

KELOMPOK_MINAT_MAP = {
    'Teknologi & Komputer': 'minat_teknologi',
    'Sains & Kesehatan': 'minat_sains',
    'Ekonomi & Bisnis': 'minat_bisnis',
    'Sosial & Hukum': 'minat_sosial',
    'Seni & Bahasa': 'minat_seni',
    'Pendidikan': 'minat_pendidikan',
}


def extract_student_features(student):
    """
    Ekstraksi fitur numerik dari nilai akademik dan jawaban kuesioner minat siswa.
    Mengembalikan dict fitur dan list array sesuai urutan FEATURE_NAMES.
    """
    # 1. Nilai akademik
    if hasattr(student, 'academic_data') and student.academic_data:
        acad = student.academic_data
        nilai_dict = {
            'nilai_matematika': float(acad.nilai_matematika),
            'nilai_bahasa_indonesia': float(acad.nilai_bahasa_indonesia),
            'nilai_bahasa_inggris': float(acad.nilai_bahasa_inggris),
            'nilai_ipa': float(acad.nilai_ipa),
            'nilai_ips': float(acad.nilai_ips),
            'nilai_agama': float(acad.nilai_agama),
        }
    else:
        nilai_dict = {k: 0.0 for k in FEATURE_NAMES[:6]}

    # 2. Minat siswa berdasarkan kelompok
    interest_scores = {k: [] for k in KELOMPOK_MINAT_MAP.values()}
    for resp in student.interest_responses.select_related('question').all():
        group_key = KELOMPOK_MINAT_MAP.get(resp.question.kelompok_minat)
        if group_key:
            interest_scores[group_key].append(resp.answer_value)

    # Rata-rata per kelompok minat (skala 1 - 5)
    minat_dict = {}
    for group_key, scores in interest_scores.items():
        if scores:
            minat_dict[group_key] = round(sum(scores) / len(scores), 2)
        else:
            minat_dict[group_key] = 3.0  # default netral jika belum ada jawaban

    features_dict = {**nilai_dict, **minat_dict}
    features_vector = [features_dict.get(feat, 0.0) for feat in FEATURE_NAMES]

    return features_dict, features_vector


def train_random_forest_model(n_estimators=100, max_depth=None, test_size=0.2, random_state=42):
    """
    Melatih model Random Forest menggunakan Scikit-learn dari seluruh TrainingRecord.
    Menghitung metrik evaluasi aktual (Accuracy, Precision, Recall, F1-Score, Confusion Matrix).
    Menyimpan model ke disk dan membuat entri ModelVersion.
    """
    from spk.models import TrainingRecord, ModelVersion
    import numpy as np

    # Import scikit-learn
    try:
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.model_selection import train_test_split
        from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
        import joblib
    except ImportError as e:
        logger.error(f"Scikit-learn atau joblib tidak ditemukan: {e}")
        return False, f"Pustaka scikit-learn / joblib belum terinstall: {e}", None

    records = list(TrainingRecord.objects.all())
    if len(records) < 10:
        return False, "Data latih terlalu sedikit (minimal 10 data untuk pelatihan model).", None

    X = []
    y = []

    for r in records:
        f_vals = r.feature_values
        row = [float(f_vals.get(feat, 0.0)) for feat in FEATURE_NAMES]
        X.append(row)
        y.append(r.major_label)

    X = np.array(X)
    y = np.array(y)

    unique_classes = np.unique(y)
    if len(unique_classes) < 2:
        return False, "Data latih harus memiliki minimal 2 kelas jurusan target yang berbeda.", None

    # Train / Test split
    try:
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state, stratify=y if len(y) >= len(unique_classes) * 2 else None
        )
    except Exception:
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state
        )

    # Inisialisasi dan pelatihan RandomForestClassifier
    rf = RandomForestClassifier(
        n_estimators=int(n_estimators),
        max_depth=int(max_depth) if max_depth else None,
        random_state=random_state
    )
    rf.fit(X_train, y_train)

    # Evaluasi pada data uji (Unseen test set)
    y_pred = rf.predict(X_test)

    acc = float(accuracy_score(y_test, y_pred))
    prec_macro = float(precision_score(y_test, y_pred, average='macro', zero_division=0))
    rec_macro = float(recall_score(y_test, y_pred, average='macro', zero_division=0))
    f1_macro = float(f1_score(y_test, y_pred, average='macro', zero_division=0))

    prec_weighted = float(precision_score(y_test, y_pred, average='weighted', zero_division=0))
    rec_weighted = float(recall_score(y_test, y_pred, average='weighted', zero_division=0))
    f1_weighted = float(f1_score(y_test, y_pred, average='weighted', zero_division=0))

    class_list = [str(c) for c in rf.classes_]
    cm = confusion_matrix(y_test, y_pred, labels=rf.classes_).tolist()

    # Feature Importance
    importances = rf.feature_importances_
    feat_importance_dict = {
        feat: float(round(imp * 100, 2))
        for feat, imp in zip(FEATURE_NAMES, importances)
    }
    # Urutkan feature importance terbesar ke terkecil
    feat_importance_sorted = sorted(
        [{'feature': f, 'label': FEATURE_LABELS[f], 'importance': imp} for f, imp in feat_importance_dict.items()],
        key=lambda x: x['importance'],
        reverse=True
    )

    # Persiapkan folder penyimpanan model
    models_dir = Path(settings.MEDIA_ROOT) / 'models'
    models_dir.mkdir(parents=True, exist_ok=True)

    timestamp_str = datetime.now().strftime('%Y%m%d_%H%M%S')
    version_code = f"RF-{timestamp_str}"
    artifact_filename = f"model_{version_code}.joblib"
    artifact_full_path = str(models_dir / artifact_filename)

    # Simpan model joblib
    joblib.dump(rf, artifact_full_path)

    # Simpan ModelVersion ke DB
    ModelVersion.objects.filter(is_active=True).update(is_active=False)

    model_ver = ModelVersion.objects.create(
        version_name=version_code,
        algorithm='Random Forest Classifier',
        parameters={
            'n_estimators': int(n_estimators),
            'max_depth': int(max_depth) if max_depth else 'None',
            'test_size': float(test_size),
            'random_state': int(random_state),
            'n_features': len(FEATURE_NAMES),
            'n_train_samples': len(X_train),
            'n_test_samples': len(X_test),
            'total_samples': len(X),
        },
        dataset_version='v1.0',
        evaluation_metrics={
            'accuracy': round(acc * 100, 2),
            'precision_macro': round(prec_macro * 100, 2),
            'recall_macro': round(rec_macro * 100, 2),
            'f1_macro': round(f1_macro * 100, 2),
            'precision_weighted': round(prec_weighted * 100, 2),
            'recall_weighted': round(rec_weighted * 100, 2),
            'f1_weighted': round(f1_weighted * 100, 2),
            'classes': class_list,
            'confusion_matrix': cm,
            'feature_importances': feat_importance_sorted
        },
        artifact_path=artifact_full_path,
        is_active=True,
        status='active'
    )

    return True, f"Model {version_code} berhasil dilatih dengan akurasi data uji {round(acc*100, 2)}%.", model_ver


def predict_for_student(student, model_ver=None):
    """
    Menjalankan proses inferensi Random Forest untuk siswa sesuai PRD FR-09, FR-10, FR-11.
    Menghasilkan detail tahapan perhitungan lengkap (Tahap 1 s/d Tahap 5).
    Menyimpan hasil ke PredictionRun dan RecommendationResult.
    """
    from spk.models import ModelVersion, PredictionRun, RecommendationResult
    import numpy as np

    try:
        import joblib
    except ImportError:
        return False, "Pustaka joblib belum terinstall.", None

    # Validasi kelengkapan data siswa
    if not student.has_complete_academics:
        return False, f"Data nilai akademik siswa {student.nama} belum lengkap.", None

    if student.status_pengisian != 'Sudah mengisi':
        return False, f"Siswa {student.nama} belum menyelesaikan pengisian formulir minat dan bakat.", None

    # Dapatkan model aktif jika tidak dispesifikasikan
    if not model_ver:
        model_ver = ModelVersion.objects.filter(is_active=True).first()

    if not model_ver:
        return False, "Belum ada model Random Forest yang aktif. Silakan latih model pada menu Data Latih terlebih dahulu.", None

    if not os.path.exists(model_ver.artifact_path):
        return False, f"File artifact model tidak ditemukan di path: {model_ver.artifact_path}", None

    try:
        rf_model = joblib.load(model_ver.artifact_path)
    except Exception as e:
        return False, f"Gagal memuat file model: {str(e)}", None

    # Ekstraksi Fitur
    features_dict, features_vector = extract_student_features(student)

    # ---------------- TAHAP 1: Data Input ----------------
    tahap_1 = {
        'nama_siswa': student.nama,
        'nis': student.nis,
        'kelas': student.kelas,
        'fitur_input': [
            {'nama_fitur': feat, 'label': FEATURE_LABELS[feat], 'nilai': features_dict[feat]}
            for feat in FEATURE_NAMES
        ],
        'keterangan': 'Identitas NIS dan nama hanya sebagai referensi siswa, bukan fitur model.'
    }

    # ---------------- TAHAP 2: Validasi & Preprocessing ----------------
    tahap_2 = {
        'status_kelengkapan': 'Lengkap & Valid',
        'urutan_fitur': FEATURE_NAMES,
        'vektor_fitur_numerik': features_vector,
        'metode_transformasi': 'Fitur nilai akademik skala 0-100 dan rata-rata kelompok minat skala 1-5 disajikan langsung ke Random Forest tanpa normalisasi (Random Forest invariant terhadap skala fitur kontinu).',
    }

    # ---------------- TAHAP 3: Informasi Model ----------------
    tahap_3 = {
        'nama_versi': model_ver.version_name,
        'algoritma': model_ver.algorithm,
        'tanggal_latih': model_ver.trained_at.strftime('%d-%m-%Y %H:%M:%S'),
        'parameters': model_ver.parameters,
        'dataset_version': model_ver.dataset_version,
    }

    # ---------------- TAHAP 4: Proses Prediksi Probabilitas ----------------
    X_input = np.array([features_vector])
    proba_array = rf_model.predict_proba(X_input)[0]
    classes = rf_model.classes_

    # Kumpulkan probabilitas seluruh kelas
    all_class_scores = []
    for cls_name, prob in zip(classes, proba_array):
        all_class_scores.append({
            'major_label': str(cls_name),
            'probability': float(prob),
            'score_percent': round(float(prob) * 100, 2)
        })

    # Urutkan berdasarkan probabilitas menurun
    all_class_scores_sorted = sorted(all_class_scores, key=lambda x: x['probability'], reverse=True)

    tahap_4 = {
        'distribusi_probabilitas': all_class_scores_sorted,
        'kelas_terpilih_argmax': str(rf_model.predict(X_input)[0]),
        'feature_importances': model_ver.evaluation_metrics.get('feature_importances', [])
    }

    # ---------------- TAHAP 5: Pengurutan Rekomendasi (Top 5) ----------------
    top_5_majors = all_class_scores_sorted[:5]
    for idx, item in enumerate(top_5_majors, 1):
        item['rank'] = idx
        item['is_primary'] = (idx == 1)

    tahap_5 = {
        'rekomendasi_teratas': top_5_majors,
        'jumlah_kelas_tersedia': len(classes),
        'rekomendasi_utama': top_5_majors[0]['major_label'] if top_5_majors else None
    }

    calculation_details = {
        'tahap_1_input': tahap_1,
        'tahap_2_preprocessing': tahap_2,
        'tahap_3_info_model': tahap_3,
        'tahap_4_prediksi': tahap_4,
        'tahap_5_ranking': tahap_5,
    }

    # ---------------- TAHAP 6: Penyimpanan Hasil ----------------
    pred_run = PredictionRun.objects.create(
        student=student,
        model_version=model_ver,
        status='Berhasil',
        input_snapshot=features_dict,
        calculation_details=calculation_details
    )

    for item in top_5_majors:
        RecommendationResult.objects.create(
            prediction_run=pred_run,
            major_label=item['major_label'],
            score=item['score_percent'],
            rank=item['rank']
        )

    # Update status prediksi siswa
    student.status_prediksi = 'Berhasil'
    student.save()

    return True, f"Prediksi untuk siswa {student.nama} berhasil diproses.", pred_run
