import csv
import io
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.http import JsonResponse, HttpResponse

from spk.models import (
    Student,
    StudentAcademicData,
    InterestQuestion,
    StudentInterestResponse,
    TrainingRecord,
    ModelVersion,
    PredictionRun,
    RecommendationResult
)
from spk.forms import (
    StudentForm,
    AcademicDataForm,
    TrainingRecordForm,
    CSVImportForm,
    ModelTrainForm
)
from spk.ml_engine import (
    train_random_forest_model,
    predict_for_student,
    FEATURE_NAMES,
    FEATURE_LABELS,
    KELOMPOK_MINAT_MAP
)


def is_admin(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser)


# ==============================================================================
# AUTHENTICATION VIEWS
# ==============================================================================

def admin_login_view(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)

        if user is not None and (user.is_staff or user.is_superuser):
            login(request, user)
            messages.success(request, f"Selamat datang, {user.username}!")
            return redirect('dashboard')
        else:
            messages.error(request, "Username atau password admin salah.")

    return render(request, 'admin/login.html')


def admin_logout_view(request):
    logout(request)
    messages.info(request, "Anda telah berhasil logout.")
    return redirect('admin_login')


# ==============================================================================
# ADMIN VIEWS (Hanya 5 menu sidebar: Dashboard, Data Siswa, Prediksi Jurusan, Data Latih, Logout)
# ==============================================================================

@user_passes_test(is_admin, login_url='admin_login')
def dashboard_view(request):
    total_siswa = Student.objects.count()
    siswa_sudah_isi = Student.objects.filter(status_pengisian='Sudah mengisi').count()
    siswa_menunggu_prediksi = Student.objects.filter(
        status_pengisian='Sudah mengisi',
        status_prediksi__in=['Menunggu', 'Perlu prediksi ulang']
    ).count()
    prediksi_berhasil = Student.objects.filter(status_prediksi='Berhasil').count()
    prediksi_gagal = Student.objects.filter(status_prediksi='Gagal').count()

    total_data_latih = TrainingRecord.objects.count()
    active_model = ModelVersion.objects.filter(is_active=True).first()

    # Jurusan yang paling sering direkomendasikan pada peringkat 1
    top_majors = (
        RecommendationResult.objects.filter(rank=1)
        .values('major_label')
        .annotate(total=Count('major_label'))
        .order_by('-total')[:6]
    )

    recent_predictions = PredictionRun.objects.select_related('student', 'model_version').order_by('-completed_at')[:5]

    context = {
        'total_siswa': total_siswa,
        'siswa_sudah_isi': siswa_sudah_isi,
        'siswa_menunggu_prediksi': siswa_menunggu_prediksi,
        'prediksi_berhasil': prediksi_berhasil,
        'prediksi_gagal': prediksi_gagal,
        'total_data_latih': total_data_latih,
        'active_model': active_model,
        'top_majors': list(top_majors),
        'recent_predictions': recent_predictions,
        'active_nav': 'dashboard'
    }
    return render(request, 'admin/dashboard.html', context)


@user_passes_test(is_admin, login_url='admin_login')
def data_siswa_view(request):
    query = request.GET.get('q', '').strip()
    status_pengisian = request.GET.get('status_pengisian', '').strip()
    status_prediksi = request.GET.get('status_prediksi', '').strip()

    students = Student.objects.select_related('academic_data').all()

    if query:
        students = students.filter(Q(nis__icontains=query) | Q(nama__icontains=query))
    if status_pengisian:
        students = students.filter(status_pengisian=status_pengisian)
    if status_prediksi:
        students = students.filter(status_prediksi=status_prediksi)

    paginator = Paginator(students, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'query': query,
        'status_pengisian': status_pengisian,
        'status_prediksi': status_prediksi,
        'active_nav': 'data_siswa'
    }
    return render(request, 'admin/data_siswa.html', context)


@user_passes_test(is_admin, login_url='admin_login')
def siswa_create_view(request):
    if request.method == 'POST':
        student_form = StudentForm(request.POST)
        academic_form = AcademicDataForm(request.POST)

        if student_form.is_valid() and academic_form.is_valid():
            student = student_form.save()
            academic = academic_form.save(commit=False)
            academic.student = student
            academic.save()
            messages.success(request, f"Data siswa {student.nama} berhasil ditambahkan.")
            return redirect('data_siswa')
        else:
            messages.error(request, "Mohon periksa kembali input formulir.")
    else:
        student_form = StudentForm()
        academic_form = AcademicDataForm()

    context = {
        'student_form': student_form,
        'academic_form': academic_form,
        'is_edit': False,
        'active_nav': 'data_siswa'
    }
    return render(request, 'admin/siswa_form.html', context)


@user_passes_test(is_admin, login_url='admin_login')
def siswa_edit_view(request, pk):
    student = get_object_or_404(Student, pk=pk)
    academic, _ = StudentAcademicData.objects.get_or_create(student=student)

    if request.method == 'POST':
        student_form = StudentForm(request.POST, instance=student)
        academic_form = AcademicDataForm(request.POST, instance=academic)

        if student_form.is_valid() and academic_form.is_valid():
            # Jika ada prediksi lama dan nilai akademik berubah, beri tanda perlu prediksi ulang (PRD AC-14)
            if student.status_prediksi == 'Berhasil':
                student.status_prediksi = 'Perlu prediksi ulang'
            student_form.save()
            academic_form.save()
            messages.success(request, f"Data siswa {student.nama} berhasil diperbarui.")
            return redirect('siswa_detail', pk=student.pk)
        else:
            messages.error(request, "Mohon periksa kembali input formulir.")
    else:
        student_form = StudentForm(instance=student)
        academic_form = AcademicDataForm(instance=academic)

    context = {
        'student_form': student_form,
        'academic_form': academic_form,
        'student': student,
        'is_edit': True,
        'active_nav': 'data_siswa'
    }
    return render(request, 'admin/siswa_form.html', context)


@user_passes_test(is_admin, login_url='admin_login')
def siswa_delete_view(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        nama = student.nama
        student.delete()
        messages.success(request, f"Data siswa {nama} berhasil dihapus.")
        return redirect('data_siswa')
    return render(request, 'admin/siswa_confirm_delete.html', {'student': student, 'active_nav': 'data_siswa'})


@user_passes_test(is_admin, login_url='admin_login')
def siswa_detail_view(request, pk):
    student = get_object_or_404(Student.objects.select_related('academic_data'), pk=pk)
    
    # Jawaban kuesioner dikelompokkan
    responses = student.interest_responses.select_related('question').order_by('question__kelompok_minat', 'question__urutan')
    
    # Kelompokkan jawaban minat
    grouped_responses = {}
    for resp in responses:
        group = resp.question.kelompok_minat
        if group not in grouped_responses:
            grouped_responses[group] = []
        grouped_responses[group].append(resp)

    # Rata-rata per kelompok minat
    group_averages = []
    for group, items in grouped_responses.items():
        avg = round(sum(i.answer_value for i in items) / len(items), 2)
        group_averages.append({'group': group, 'average': avg})

    predictions = student.prediction_runs.prefetch_related('results').order_by('-completed_at')

    context = {
        'student': student,
        'grouped_responses': grouped_responses,
        'group_averages': group_averages,
        'predictions': predictions,
        'active_nav': 'data_siswa'
    }
    return render(request, 'admin/siswa_detail.html', context)


# ------------------------------------------------------------------------------
# DATA LATIH & PELATIHAN MODEL
# ------------------------------------------------------------------------------

@user_passes_test(is_admin, login_url='admin_login')
def data_latih_view(request):
    query = request.GET.get('q', '').strip()
    label_filter = request.GET.get('major_label', '').strip()

    records = TrainingRecord.objects.all()
    if query:
        records = records.filter(Q(major_label__icontains=query) | Q(dataset_version__icontains=query))
    if label_filter:
        records = records.filter(major_label=label_filter)

    distinct_majors = TrainingRecord.objects.values_list('major_label', flat=True).distinct().order_by('major_label')

    paginator = Paginator(records, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    active_model = ModelVersion.objects.filter(is_active=True).first()
    all_models = ModelVersion.objects.order_by('-trained_at')[:10]

    train_form = ModelTrainForm()
    csv_form = CSVImportForm()

    context = {
        'page_obj': page_obj,
        'query': query,
        'label_filter': label_filter,
        'distinct_majors': distinct_majors,
        'total_records': TrainingRecord.objects.count(),
        'active_model': active_model,
        'all_models': all_models,
        'train_form': train_form,
        'csv_form': csv_form,
        'feature_labels': FEATURE_LABELS,
        'active_nav': 'data_latih'
    }
    return render(request, 'admin/data_latih.html', context)


@user_passes_test(is_admin, login_url='admin_login')
def data_latih_create_view(request):
    if request.method == 'POST':
        form = TrainingRecordForm(request.POST)
        if form.is_valid():
            major = form.cleaned_data['major_label']
            version = form.cleaned_data['dataset_version']

            feature_values = {
                feat: form.cleaned_data[feat] for feat in FEATURE_NAMES
            }

            TrainingRecord.objects.create(
                feature_values=feature_values,
                major_label=major,
                dataset_version=version
            )
            messages.success(request, f"Data latih jurusan {major} berhasil ditambahkan.")
            return redirect('data_latih')
    else:
        form = TrainingRecordForm()

    return render(request, 'admin/data_latih_form.html', {'form': form, 'active_nav': 'data_latih'})


@user_passes_test(is_admin, login_url='admin_login')
def data_latih_delete_view(request, pk):
    record = get_object_or_404(TrainingRecord, pk=pk)
    if request.method == 'POST':
        record.delete()
        messages.success(request, "Data latih berhasil dihapus.")
        return redirect('data_latih')
    return render(request, 'admin/data_latih_confirm_delete.html', {'record': record, 'active_nav': 'data_latih'})


@user_passes_test(is_admin, login_url='admin_login')
def data_latih_import_csv_view(request):
    if request.method == 'POST':
        form = CSVImportForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            dataset_version = form.cleaned_data['dataset_version']

            if not csv_file.name.endswith('.csv'):
                messages.error(request, "File harus berformat .csv")
                return redirect('data_latih')

            try:
                decoded_file = csv_file.read().decode('utf-8')
                io_string = io.StringIO(decoded_file)
                reader = csv.DictReader(io_string)

                created_count = 0
                for row in reader:
                    major = row.get('major_label') or row.get('jurusan') or row.get('label')
                    if not major:
                        continue

                    feature_values = {}
                    for feat in FEATURE_NAMES:
                        try:
                            feature_values[feat] = float(row.get(feat, 0.0))
                        except (ValueError, TypeError):
                            feature_values[feat] = 0.0

                    TrainingRecord.objects.create(
                        feature_values=feature_values,
                        major_label=major.strip(),
                        dataset_version=dataset_version
                    )
                    created_count += 1

                messages.success(request, f"Berhasil mengimpor {created_count} data latih dari CSV.")
            except Exception as e:
                messages.error(request, f"Gagal memproses file CSV: {str(e)}")

    return redirect('data_latih')


@user_passes_test(is_admin, login_url='admin_login')
def model_train_view(request):
    if request.method == 'POST':
        form = ModelTrainForm(request.POST)
        if form.is_valid():
            n_est = form.cleaned_data['n_estimators']
            depth = form.cleaned_data['max_depth']
            t_size = form.cleaned_data['test_size']
            r_state = form.cleaned_data['random_state']

            success, msg, model_ver = train_random_forest_model(
                n_estimators=n_est,
                max_depth=depth,
                test_size=t_size,
                random_state=r_state
            )

            if success:
                messages.success(request, msg)
            else:
                messages.error(request, msg)
        else:
            messages.error(request, "Parameter pelatihan model tidak valid.")

    return redirect('data_latih')


# ------------------------------------------------------------------------------
# PREDIKSI JURUSAN & DETAIL PERHITUNGAN
# ------------------------------------------------------------------------------

@user_passes_test(is_admin, login_url='admin_login')
def prediksi_jurusan_view(request):
    tab = request.GET.get('tab', 'siap')  # 'siap' atau 'riwayat'
    query = request.GET.get('q', '').strip()

    active_model = ModelVersion.objects.filter(is_active=True).first()

    # Siswa yang siap diprediksi: sudah mengisi kuesioner dan nilai akademik lengkap
    ready_students = (
        Student.objects.select_related('academic_data')
        .filter(status_pengisian='Sudah mengisi')
        .order_by('status_prediksi', 'nis')
    )

    if query:
        ready_students = ready_students.filter(Q(nis__icontains=query) | Q(nama__icontains=query))

    # Riwayat prediksi
    history_runs = (
        PredictionRun.objects.select_related('student', 'model_version')
        .prefetch_related('results')
        .order_by('-completed_at')
    )
    if query:
        history_runs = history_runs.filter(Q(student__nis__icontains=query) | Q(student__nama__icontains=query))

    paginator_ready = Paginator(ready_students, 10)
    page_ready = paginator_ready.get_page(request.GET.get('page'))

    paginator_hist = Paginator(history_runs, 10)
    page_hist = paginator_hist.get_page(request.GET.get('page'))

    context = {
        'tab': tab,
        'query': query,
        'active_model': active_model,
        'page_ready': page_ready,
        'page_hist': page_hist,
        'total_ready': ready_students.count(),
        'total_hist': history_runs.count(),
        'active_nav': 'prediksi_jurusan'
    }
    return render(request, 'admin/prediksi_jurusan.html', context)


@user_passes_test(is_admin, login_url='admin_login')
def run_prediction_single_view(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    success, msg, pred_run = predict_for_student(student)

    if success:
        messages.success(request, msg)
        return redirect('prediksi_detail', pk=pred_run.pk)
    else:
        # Jika gagal, catat kegagalan (PRD FR-09 & AC-12)
        student.status_prediksi = 'Gagal'
        student.save()
        PredictionRun.objects.create(
            student=student,
            status='Gagal',
            error_message=msg
        )
        messages.error(request, msg)
        return redirect('prediksi_jurusan')


@user_passes_test(is_admin, login_url='admin_login')
def run_prediction_batch_view(request):
    if request.method == 'POST':
        student_ids = request.POST.getlist('selected_students')
        if not student_ids:
            messages.warning(request, "Pilih minimal satu siswa untuk diprediksi secara batch.")
            return redirect('prediksi_jurusan')

        success_count = 0
        fail_count = 0

        for s_id in student_ids:
            try:
                student = Student.objects.get(pk=s_id)
                success, msg, _ = predict_for_student(student)
                if success:
                    success_count += 1
                else:
                    fail_count += 1
            except Exception:
                fail_count += 1

        messages.info(request, f"Proses batch selesai: {success_count} berhasil, {fail_count} gagal.")
    return redirect('prediksi_jurusan')


@user_passes_test(is_admin, login_url='admin_login')
def prediksi_detail_view(request, pk):
    """
    Menampilkan transparansi tahapan perhitungan (Tahap 1 s/d 5) sesuai FR-10.
    """
    pred_run = get_object_or_404(
        PredictionRun.objects.select_related('student', 'model_version').prefetch_related('results'),
        pk=pk
    )
    details = pred_run.calculation_details or {}

    context = {
        'pred_run': pred_run,
        'details': details,
        'tahap_1': details.get('tahap_1_input', {}),
        'tahap_2': details.get('tahap_2_preprocessing', {}),
        'tahap_3': details.get('tahap_3_info_model', {}),
        'tahap_4': details.get('tahap_4_prediksi', {}),
        'tahap_5': details.get('tahap_5_ranking', {}),
        'results': pred_run.results.order_by('rank'),
        'active_nav': 'prediksi_jurusan'
    }
    return render(request, 'admin/prediksi_detail.html', context)


# ==============================================================================
# SISWA VIEWS (Alur Cek NIS, Pengisian Formulir, Menunggu, Hasil Rekomendasi)
# ==============================================================================

def cek_nis_view(request):
    """
    Halaman utama siswa: Cek NIS untuk verifikasi identitas (FR-01, FR-04).
    """
    if request.method == 'POST':
        nis = request.POST.get('nis', '').strip()
        if not nis:
            messages.error(request, "Silakan masukkan Nomor Induk Siswa (NIS).")
            return render(request, 'siswa/cek_nis.html')

        try:
            student = Student.objects.select_related('academic_data').get(nis=nis)
            # Simpan sesi siswa
            request.session['student_id'] = student.id
            request.session['student_nis'] = student.nis
            request.session['student_nama'] = student.nama

            # Alur berdasarkan status pengisian dan prediksi
            if student.status_pengisian != 'Sudah mengisi':
                return redirect('formulir_minat')
            elif student.status_prediksi == 'Berhasil':
                return redirect('hasil_rekomendasi')
            else:
                return redirect('status_menunggu')

        except Student.DoesNotExist:
            messages.error(request, f"Data dengan NIS '{nis}' tidak ditemukan. Silakan hubungi Guru BK / Admin MA Plus Peradaban Insani.")

    return render(request, 'siswa/cek_nis.html')


def formulir_minat_view(request):
    """
    Formulir minat & bakat siswa (skala Likert 1-5).
    """
    student_id = request.session.get('student_id')
    if not student_id:
        messages.warning(request, "Silakan masukkan NIS terlebih dahulu.")
        return redirect('cek_nis')

    student = get_object_or_404(Student.objects.select_related('academic_data'), pk=student_id)

    # Ambil pertanyaan aktif yang dikelompokkan
    questions = InterestQuestion.objects.filter(is_active=True).order_by('urutan', 'kode_pertanyaan')
    grouped_questions = {}
    for q in questions:
        group = q.kelompok_minat
        if group not in grouped_questions:
            grouped_questions[group] = []
        grouped_questions[group].append(q)

    # Ambil jawaban terdahulu jika sudah pernah mengisi
    existing_responses = {
        resp.question_id: resp.answer_value
        for resp in student.interest_responses.all()
    }

    if request.method == 'POST':
        unanswered = []
        answers_to_save = []

        for q in questions:
            field_name = f"question_{q.id}"
            val = request.POST.get(field_name)
            if not val:
                unanswered.append(q.kode_pertanyaan)
            else:
                try:
                    score = int(val)
                    if 1 <= score <= 5:
                        answers_to_save.append((q, score))
                    else:
                        unanswered.append(q.kode_pertanyaan)
                except ValueError:
                    unanswered.append(q.kode_pertanyaan)

        if unanswered:
            messages.error(request, f"Harap lengkapi semua pertanyaan! Ada {len(unanswered)} pertanyaan yang belum dijawab.")
        else:
            # Simpan seluruh jawaban
            for q, score in answers_to_save:
                StudentInterestResponse.objects.update_or_create(
                    student=student,
                    question=q,
                    defaults={'answer_value': score}
                )

            student.status_pengisian = 'Sudah mengisi'
            # Jika sebelumnya sudah diprediksi, tandai perlu prediksi ulang (PRD AC-14)
            if student.status_prediksi == 'Berhasil':
                student.status_prediksi = 'Perlu prediksi ulang'
            else:
                student.status_prediksi = 'Menunggu'
            student.save()

            messages.success(request, "Terima kasih! Formulir minat dan bakat Anda telah berhasil disimpan.")
            return redirect('status_menunggu')

    context = {
        'student': student,
        'grouped_questions': grouped_questions,
        'existing_responses': existing_responses,
        'total_questions': questions.count(),
    }
    return render(request, 'siswa/formulir_minat.html', context)


def status_menunggu_view(request):
    """
    Halaman konfirmasi pengiriman & status menunggu prediksi (FR-05, FR-12).
    """
    student_id = request.session.get('student_id')
    if not student_id:
        return redirect('cek_nis')

    student = get_object_or_404(Student, pk=student_id)

    # Jika sudah diprediksi dan berhasil, arahkan ke hasil
    if student.status_prediksi == 'Berhasil':
        return redirect('hasil_rekomendasi')

    context = {
        'student': student
    }
    return render(request, 'siswa/status_menunggu.html', context)


def hasil_rekomendasi_view(request):
    """
    Halaman hasil rekomendasi 5 jurusan teratas bagi siswa (FR-11, FR-12).
    Siswa hanya dapat melihat hasil miliknya sendiri (AC-11).
    """
    student_id = request.session.get('student_id')
    if not student_id:
        messages.warning(request, "Silakan masukkan NIS Anda.")
        return redirect('cek_nis')

    student = get_object_or_404(Student, pk=student_id)

    if student.status_prediksi != 'Berhasil':
        messages.info(request, "Hasil rekomendasi Anda belum diproses atau masih dalam antrean.")
        return redirect('status_menunggu')

    latest_run = student.prediction_runs.filter(status='Berhasil').order_by('-completed_at').first()

    if not latest_run:
        messages.warning(request, "Data rekomendasi belum tersedia.")
        return redirect('status_menunggu')

    results = latest_run.results.order_by('rank')[:5]
    primary_recommendation = results.first() if results.exists() else None

    # Snapshot data minat untuk visualisasi profil siswa
    features_dict = latest_run.input_snapshot or {}
    interest_profiles = [
        {'label': 'Teknologi & Komputer', 'score': features_dict.get('minat_teknologi', 3.0)},
        {'label': 'Sains & Kesehatan', 'score': features_dict.get('minat_sains', 3.0)},
        {'label': 'Ekonomi & Bisnis', 'score': features_dict.get('minat_bisnis', 3.0)},
        {'label': 'Sosial & Hukum', 'score': features_dict.get('minat_sosial', 3.0)},
        {'label': 'Seni & Desain', 'score': features_dict.get('minat_seni', 3.0)},
        {'label': 'Pendidikan & Bahasa', 'score': features_dict.get('minat_pendidikan', 3.0)},
    ]

    context = {
        'student': student,
        'latest_run': latest_run,
        'results': results,
        'primary_recommendation': primary_recommendation,
        'interest_profiles': interest_profiles,
        'features_dict': features_dict,
    }
    return render(request, 'siswa/hasil_rekomendasi.html', context)


def siswa_logout_view(request):
    """
    Mengakhiri sesi pengecekan siswa.
    """
    request.session.flush()
    messages.info(request, "Sesi Anda telah selesai.")
    return redirect('cek_nis')
