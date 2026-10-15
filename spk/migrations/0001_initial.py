from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='InterestQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kode_pertanyaan', models.CharField(max_length=20, unique=True, verbose_name='Kode Pertanyaan')),
                ('teks_pertanyaan', models.TextField(verbose_name='Teks Pertanyaan')),
                ('kelompok_minat', models.CharField(choices=[('Teknologi & Komputer', 'Teknologi & Komputer'), ('Sains & Kesehatan', 'Sains & Kesehatan'), ('Ekonomi & Bisnis', 'Ekonomi & Bisnis'), ('Sosial & Hukum', 'Sosial & Hukum'), ('Seni & Bahasa', 'Seni & Bahasa'), ('Pendidikan', 'Pendidikan')], max_length=50, verbose_name='Kelompok Minat')),
                ('tipe_jawaban', models.CharField(default='skala_likert', max_length=30, verbose_name='Tipe Jawaban')),
                ('skala_minimum', models.IntegerField(default=1, verbose_name='Skala Minimum')),
                ('skala_maksimum', models.IntegerField(default=5, verbose_name='Skala Maksimum')),
                ('is_active', models.BooleanField(default=True, verbose_name='Aktif')),
                ('urutan', models.IntegerField(default=0, verbose_name='Urutan Tampil')),
            ],
            options={
                'verbose_name': 'Pertanyaan Minat & Bakat',
                'verbose_name_plural': 'Pertanyaan Minat & Bakat',
                'ordering': ['urutan', 'kode_pertanyaan'],
            },
        ),
        migrations.CreateModel(
            name='ModelVersion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('version_name', models.CharField(max_length=50, unique=True, verbose_name='Nama Versi')),
                ('algorithm', models.CharField(default='Random Forest Classifier', max_length=100, verbose_name='Algoritma')),
                ('parameters', models.JSONField(default=dict, verbose_name='Hyperparameter')),
                ('dataset_version', models.CharField(default='v1.0', max_length=50, verbose_name='Versi Dataset')),
                ('evaluation_metrics', models.JSONField(default=dict, verbose_name='Hasil Evaluasi')),
                ('artifact_path', models.CharField(max_length=255, verbose_name='Path File Model (.joblib)')),
                ('is_active', models.BooleanField(default=False, verbose_name='Model Aktif')),
                ('trained_at', models.DateTimeField(auto_now_add=True, verbose_name='Waktu Pelatihan')),
                ('status', models.CharField(default='active', max_length=30, verbose_name='Status Model')),
            ],
            options={
                'verbose_name': 'Versi Model',
                'verbose_name_plural': 'Versi Model',
                'ordering': ['-trained_at'],
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nis', models.CharField(max_length=20, unique=True, verbose_name='NIS')),
                ('nama', models.CharField(max_length=150, verbose_name='Nama Lengkap')),
                ('kelas', models.CharField(default='XII IPA', max_length=50, verbose_name='Kelas')),
                ('tahun_ajaran', models.CharField(default='2024/2025', max_length=20, verbose_name='Tahun Ajaran')),
                ('status_pengisian', models.CharField(choices=[('Belum mengisi', 'Belum mengisi'), ('Sudah mengisi', 'Sudah mengisi'), ('Perlu melengkapi data', 'Perlu melengkapi data')], default='Belum mengisi', max_length=30, verbose_name='Status Pengisian Formulir')),
                ('status_prediksi', models.CharField(choices=[('Menunggu', 'Menunggu'), ('Diproses', 'Diproses'), ('Berhasil', 'Berhasil'), ('Gagal', 'Gagal'), ('Perlu prediksi ulang', 'Perlu prediksi ulang')], default='Menunggu', max_length=30, verbose_name='Status Prediksi')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Dibuat Pada')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Diperbarui Pada')),
            ],
            options={
                'verbose_name': 'Data Siswa',
                'verbose_name_plural': 'Data Siswa',
                'ordering': ['nis'],
            },
        ),
        migrations.CreateModel(
            name='TrainingRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feature_values', models.JSONField(verbose_name='Nilai Fitur Pelatihan')),
                ('major_label', models.CharField(max_length=100, verbose_name='Label Jurusan Target')),
                ('dataset_version', models.CharField(default='v1.0', max_length=50, verbose_name='Versi Dataset')),
                ('source_info', models.CharField(default='Alumni MA Plus Peradaban Insani', max_length=150, verbose_name='Sumber Data')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Dibuat Pada')),
            ],
            options={
                'verbose_name': 'Data Latih',
                'verbose_name_plural': 'Data Latih',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='PredictionRun',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('Menunggu', 'Menunggu'), ('Diproses', 'Diproses'), ('Berhasil', 'Berhasil'), ('Gagal', 'Gagal')], default='Berhasil', max_length=30, verbose_name='Status Prediksi')),
                ('input_snapshot', models.JSONField(default=dict, verbose_name='Snapshot Data Input')),
                ('calculation_details', models.JSONField(default=dict, verbose_name='Detail Tahapan Perhitungan')),
                ('error_message', models.TextField(blank=True, null=True, verbose_name='Pesan Error (Jika Gagal)')),
                ('started_at', models.DateTimeField(auto_now_add=True, verbose_name='Waktu Mulai')),
                ('completed_at', models.DateTimeField(auto_now=True, verbose_name='Waktu Selesai')),
                ('model_version', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='spk.modelversion', verbose_name='Versi Model')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prediction_runs', to='spk.student', verbose_name='Siswa')),
            ],
            options={
                'verbose_name': 'Riwayat Prediksi',
                'verbose_name_plural': 'Riwayat Prediksi',
                'ordering': ['-completed_at'],
            },
        ),
        migrations.CreateModel(
            name='RecommendationResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('major_label', models.CharField(max_length=100, verbose_name='Jurusan Rekomendasi')),
                ('score', models.FloatField(verbose_name='Skor Probabilitas (%)')),
                ('rank', models.IntegerField(verbose_name='Peringkat (1-5)')),
                ('prediction_run', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='results', to='spk.predictionrun', verbose_name='Proses Prediksi')),
            ],
            options={
                'verbose_name': 'Hasil Rekomendasi Jurusan',
                'verbose_name_plural': 'Hasil Rekomendasi Jurusan',
                'ordering': ['rank'],
            },
        ),
        migrations.CreateModel(
            name='StudentAcademicData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nilai_matematika', models.FloatField(default=0.0, verbose_name='Nilai Matematika')),
                ('nilai_bahasa_indonesia', models.FloatField(default=0.0, verbose_name='Nilai Bahasa Indonesia')),
                ('nilai_bahasa_inggris', models.FloatField(default=0.0, verbose_name='Nilai Bahasa Inggris')),
                ('nilai_ipa', models.FloatField(default=0.0, verbose_name='Nilai IPA (Fisika/Biologi/Kimia)')),
                ('nilai_ips', models.FloatField(default=0.0, verbose_name='Nilai IPS (Ekonomi/Geografi/Sosiologi)')),
                ('nilai_agama', models.FloatField(default=0.0, verbose_name='Nilai Pendidikan Agama Islam')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Terakhir Diperbarui')),
                ('student', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='academic_data', to='spk.student', verbose_name='Siswa')),
            ],
            options={
                'verbose_name': 'Nilai Akademik Siswa',
                'verbose_name_plural': 'Nilai Akademik Siswa',
            },
        ),
        migrations.CreateModel(
            name='StudentInterestResponse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer_value', models.IntegerField(default=3, verbose_name='Nilai Jawaban (1-5)')),
                ('submitted_at', models.DateTimeField(auto_now=True, verbose_name='Waktu Pengisian')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='spk.interestquestion', verbose_name='Pertanyaan')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='interest_responses', to='spk.student', verbose_name='Siswa')),
            ],
            options={
                'verbose_name': 'Jawaban Minat Siswa',
                'verbose_name_plural': 'Jawaban Minat Siswa',
                'unique_together': {('student', 'question')},
            },
        ),
    ]
