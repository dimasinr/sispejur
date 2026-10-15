from django.db import models


class Student(models.Model):
    STATUS_PENGISIAN_CHOICES = [
        ('Belum mengisi', 'Belum mengisi'),
        ('Sudah mengisi', 'Sudah mengisi'),
        ('Perlu melengkapi data', 'Perlu melengkapi data'),
    ]

    STATUS_PREDIKSI_CHOICES = [
        ('Menunggu', 'Menunggu'),
        ('Diproses', 'Diproses'),
        ('Berhasil', 'Berhasil'),
        ('Gagal', 'Gagal'),
        ('Perlu prediksi ulang', 'Perlu prediksi ulang'),
    ]

    nis = models.CharField(max_length=20, unique=True, verbose_name="NIS")
    nama = models.CharField(max_length=150, verbose_name="Nama Lengkap")
    kelas = models.CharField(max_length=50, default="XII IPA", verbose_name="Kelas")
    tahun_ajaran = models.CharField(max_length=20, default="2024/2025", verbose_name="Tahun Ajaran")
    
    status_pengisian = models.CharField(
        max_length=30,
        choices=STATUS_PENGISIAN_CHOICES,
        default='Belum mengisi',
        verbose_name="Status Pengisian Formulir"
    )
    status_prediksi = models.CharField(
        max_length=30,
        choices=STATUS_PREDIKSI_CHOICES,
        default='Menunggu',
        verbose_name="Status Prediksi"
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Dibuat Pada")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Diperbarui Pada")

    class Meta:
        verbose_name = "Data Siswa"
        verbose_name_plural = "Data Siswa"
        ordering = ['nis']

    def __str__(self):
        return f"{self.nis} - {self.nama}"

    @property
    def has_complete_academics(self):
        if not hasattr(self, 'academic_data') or self.academic_data is None:
            return False
        return self.academic_data.is_complete()

    @property
    def is_ready_for_prediction(self):
        return self.status_pengisian == 'Sudah mengisi' and self.has_complete_academics

    @property
    def latest_prediction(self):
        return self.prediction_runs.filter(status='Berhasil').order_by('-completed_at').first()


class StudentAcademicData(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE, related_name='academic_data', verbose_name="Siswa")
    nilai_matematika = models.FloatField(default=0.0, verbose_name="Nilai Matematika")
    nilai_bahasa_indonesia = models.FloatField(default=0.0, verbose_name="Nilai Bahasa Indonesia")
    nilai_bahasa_inggris = models.FloatField(default=0.0, verbose_name="Nilai Bahasa Inggris")
    nilai_ipa = models.FloatField(default=0.0, verbose_name="Nilai IPA (Fisika/Biologi/Kimia)")
    nilai_ips = models.FloatField(default=0.0, verbose_name="Nilai IPS (Ekonomi/Geografi/Sosiologi)")
    nilai_agama = models.FloatField(default=0.0, verbose_name="Nilai Pendidikan Agama Islam")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Terakhir Diperbarui")

    class Meta:
        verbose_name = "Nilai Akademik Siswa"
        verbose_name_plural = "Nilai Akademik Siswa"

    def __str__(self):
        return f"Nilai Akademik - {self.student.nama}"

    def is_complete(self):
        scores = [
            self.nilai_matematika,
            self.nilai_bahasa_indonesia,
            self.nilai_bahasa_inggris,
            self.nilai_ipa,
            self.nilai_ips,
            self.nilai_agama
        ]
        return all(s > 0 for s in scores)

    def average_score(self):
        scores = [
            self.nilai_matematika,
            self.nilai_bahasa_indonesia,
            self.nilai_bahasa_inggris,
            self.nilai_ipa,
            self.nilai_ips,
            self.nilai_agama
        ]
        return round(sum(scores) / len(scores), 2) if scores else 0.0

    def as_dict(self):
        return {
            'nilai_matematika': self.nilai_matematika,
            'nilai_bahasa_indonesia': self.nilai_bahasa_indonesia,
            'nilai_bahasa_inggris': self.nilai_bahasa_inggris,
            'nilai_ipa': self.nilai_ipa,
            'nilai_ips': self.nilai_ips,
            'nilai_agama': self.nilai_agama,
            'rata_rata': self.average_score()
        }


class InterestQuestion(models.Model):
    KELOMPOK_CHOICES = [
        ('Teknologi & Komputer', 'Teknologi & Komputer'),
        ('Sains & Kesehatan', 'Sains & Kesehatan'),
        ('Ekonomi & Bisnis', 'Ekonomi & Bisnis'),
        ('Sosial & Hukum', 'Sosial & Hukum'),
        ('Seni & Bahasa', 'Seni & Bahasa'),
        ('Pendidikan', 'Pendidikan'),
    ]

    kode_pertanyaan = models.CharField(max_length=20, unique=True, verbose_name="Kode Pertanyaan")
    teks_pertanyaan = models.TextField(verbose_name="Teks Pertanyaan")
    kelompok_minat = models.CharField(max_length=50, choices=KELOMPOK_CHOICES, verbose_name="Kelompok Minat")
    tipe_jawaban = models.CharField(max_length=30, default='skala_likert', verbose_name="Tipe Jawaban")
    skala_minimum = models.IntegerField(default=1, verbose_name="Skala Minimum")
    skala_maksimum = models.IntegerField(default=5, verbose_name="Skala Maksimum")
    is_active = models.BooleanField(default=True, verbose_name="Aktif")
    urutan = models.IntegerField(default=0, verbose_name="Urutan Tampil")

    class Meta:
        verbose_name = "Pertanyaan Minat & Bakat"
        verbose_name_plural = "Pertanyaan Minat & Bakat"
        ordering = ['urutan', 'kode_pertanyaan']

    def __str__(self):
        return f"[{self.kode_pertanyaan}] {self.kelompok_minat}: {self.teks_pertanyaan[:60]}"


class StudentInterestResponse(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='interest_responses', verbose_name="Siswa")
    question = models.ForeignKey(InterestQuestion, on_delete=models.CASCADE, verbose_name="Pertanyaan")
    answer_value = models.IntegerField(default=3, verbose_name="Nilai Jawaban (1-5)")
    submitted_at = models.DateTimeField(auto_now=True, verbose_name="Waktu Pengisian")

    class Meta:
        verbose_name = "Jawaban Minat Siswa"
        verbose_name_plural = "Jawaban Minat Siswa"
        unique_together = ('student', 'question')

    def __str__(self):
        return f"{self.student.nis} - {self.question.kode_pertanyaan}: {self.answer_value}"


class TrainingRecord(models.Model):
    feature_values = models.JSONField(verbose_name="Nilai Fitur Pelatihan")
    major_label = models.CharField(max_length=100, verbose_name="Label Jurusan Target")
    dataset_version = models.CharField(max_length=50, default='v1.0', verbose_name="Versi Dataset")
    source_info = models.CharField(max_length=150, default='Alumni MA Plus Peradaban Insani', verbose_name="Sumber Data")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Dibuat Pada")

    class Meta:
        verbose_name = "Data Latih"
        verbose_name_plural = "Data Latih"
        ordering = ['-id']

    def __str__(self):
        return f"Data Latih #{self.id} - {self.major_label} ({self.dataset_version})"


class ModelVersion(models.Model):
    version_name = models.CharField(max_length=50, unique=True, verbose_name="Nama Versi")
    algorithm = models.CharField(max_length=100, default='Random Forest Classifier', verbose_name="Algoritma")
    parameters = models.JSONField(default=dict, verbose_name="Hyperparameter")
    dataset_version = models.CharField(max_length=50, default='v1.0', verbose_name="Versi Dataset")
    evaluation_metrics = models.JSONField(default=dict, verbose_name="Hasil Evaluasi")
    artifact_path = models.CharField(max_length=255, verbose_name="Path File Model (.joblib)")
    is_active = models.BooleanField(default=False, verbose_name="Model Aktif")
    trained_at = models.DateTimeField(auto_now_add=True, verbose_name="Waktu Pelatihan")
    status = models.CharField(max_length=30, default='active', verbose_name="Status Model")

    class Meta:
        verbose_name = "Versi Model"
        verbose_name_plural = "Versi Model"
        ordering = ['-trained_at']

    def __str__(self):
        active_str = " (Aktif)" if self.is_active else ""
        return f"{self.version_name} - {self.algorithm}{active_str}"


class PredictionRun(models.Model):
    STATUS_CHOICES = [
        ('Menunggu', 'Menunggu'),
        ('Diproses', 'Diproses'),
        ('Berhasil', 'Berhasil'),
        ('Gagal', 'Gagal'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='prediction_runs', verbose_name="Siswa")
    model_version = models.ForeignKey(ModelVersion, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Versi Model")
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='Berhasil', verbose_name="Status Prediksi")
    input_snapshot = models.JSONField(default=dict, verbose_name="Snapshot Data Input")
    calculation_details = models.JSONField(default=dict, verbose_name="Detail Tahapan Perhitungan")
    error_message = models.TextField(blank=True, null=True, verbose_name="Pesan Error (Jika Gagal)")
    started_at = models.DateTimeField(auto_now_add=True, verbose_name="Waktu Mulai")
    completed_at = models.DateTimeField(auto_now=True, verbose_name="Waktu Selesai")

    class Meta:
        verbose_name = "Riwayat Prediksi"
        verbose_name_plural = "Riwayat Prediksi"
        ordering = ['-completed_at']

    def __str__(self):
        return f"Prediksi {self.student.nama} ({self.status}) - {self.completed_at.strftime('%Y-%m-%d %H:%M')}"


class RecommendationResult(models.Model):
    prediction_run = models.ForeignKey(PredictionRun, on_delete=models.CASCADE, related_name='results', verbose_name="Proses Prediksi")
    major_label = models.CharField(max_length=100, verbose_name="Jurusan Rekomendasi")
    score = models.FloatField(verbose_name="Skor Probabilitas (%)")
    rank = models.IntegerField(verbose_name="Peringkat (1-5)")

    class Meta:
        verbose_name = "Hasil Rekomendasi Jurusan"
        verbose_name_plural = "Hasil Rekomendasi Jurusan"
        ordering = ['rank']

    def __str__(self):
        return f"Peringkat {self.rank}: {self.major_label} ({self.score:.1f}%)"
