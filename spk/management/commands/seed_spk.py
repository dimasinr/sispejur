import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from spk.models import (
    Student,
    StudentAcademicData,
    InterestQuestion,
    StudentInterestResponse,
    TrainingRecord,
    ModelVersion
)
from spk.ml_engine import train_random_forest_model, predict_for_student, FEATURE_NAMES


class Command(BaseCommand):
    help = 'Seed database dengan data awal: Admin, Instrumen Pertanyaan, Data Latih Alumni, Model RF Awal, dan Contoh Siswa'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Memulai seeding data SPK MA Plus Peradaban Insani..."))

        # 1. Buat User Admin
        admin_user, created = User.objects.get_or_create(username='admin')
        admin_user.set_password('admin123')
        admin_user.is_staff = True
        admin_user.is_superuser = True
        admin_user.save()
        if created:
            self.stdout.write(self.style.SUCCESS("Akun admin berhasil dibuat (username: admin, pass: admin123)"))
        else:
            self.stdout.write(self.style.SUCCESS("Akun admin diperbarui (username: admin, pass: admin123)"))

        # 2. Seed Pertanyaan Minat & Bakat
        questions_data = [
            # Teknologi & Komputer
            ('Q01', 'Saya sangat tertarik mempelajari logika algoritma, coding, dan pemrograman aplikasi perangkat lunak.', 'Teknologi & Komputer', 1),
            ('Q02', 'Saya senang mencari tahu cara kerja perangkat keras komputer, konfigurasi jaringan, dan keamanan siber.', 'Teknologi & Komputer', 2),
            ('Q03', 'Saya penasaran dan tertarik mengembangkan teknologi kecerdasan buatan (AI) serta pengolahan data digital.', 'Teknologi & Komputer', 3),

            # Sains & Kesehatan
            ('Q04', 'Saya tertarik mendalami struktur tubuh manusia, ilmu biologi medis, dan tata cara menangani pasien yang sakit.', 'Sains & Kesehatan', 4),
            ('Q05', 'Saya senang mempelajari reaksi zat kimia, komposisi senyawa obat-obatan, dan penelitian laboratorium farmasi.', 'Sains & Kesehatan', 5),
            ('Q06', 'Saya antusias melakukan investigasi ilmiah mengenai fenomena alam, ekosistem hayati, dan sains murni.', 'Sains & Kesehatan', 6),

            # Ekonomi & Bisnis
            ('Q07', 'Saya tertarik membuat perencanaan strategi bisnis, model kewirausahaan, dan tata kelola manajemen tim.', 'Ekonomi & Bisnis', 7),
            ('Q08', 'Saya teliti dan gemar mengelola pencatatan keuangan, perhitungan neraca laba-rugi, serta laporan akuntansi.', 'Ekonomi & Bisnis', 8),
            ('Q09', 'Saya tertarik mengamati dinamika pasar modal investasi, perbankan, dan perkembangan perekonomian nasional.', 'Ekonomi & Bisnis', 9),

            # Sosial & Hukum
            ('Q10', 'Saya tertarik mempelajari undang-undang peradilan, advokasi pembelaan keadilan, dan sistem kepatuhan hukum.', 'Sosial & Hukum', 10),
            ('Q11', 'Saya senang mendengarkan permasalahan orang lain, mengamati kebiasaan perilaku, dan mempelajari psikologi.', 'Sosial & Hukum', 11),
            ('Q12', 'Saya gemar berdiskusi mengenai isu kebijakan publik, sosiologi masyarakat, dan hubungan antar bangsa.', 'Sosial & Hukum', 12),

            # Seni & Bahasa
            ('Q13', 'Saya gemar merancang karya visual estetik, ilustrasi desain grafis, tipografi kreatif, atau animasi digital.', 'Seni & Bahasa', 13),
            ('Q14', 'Saya tertarik pada produksi konten multimedia, teknik sinematografi, fotografi, dan komunikasi media massa.', 'Seni & Bahasa', 14),
            ('Q15', 'Saya senang mendalami sastra, tata bahasa asing (Arab/Inggris), penerjemahan bahasa, dan penulisan kreatif.', 'Seni & Bahasa', 15),

            # Pendidikan
            ('Q16', 'Saya memiliki tekad kuat untuk mengajarkan nilai-nilai agama Islam, akidah akhlak, dan ilmu Al-Qur\'an.', 'Pendidikan', 16),
            ('Q17', 'Saya memiliki kepuasan tersendiri saat mampu menerangkan materi pelajaran dan mendidik generasi muda.', 'Pendidikan', 17),
            ('Q18', 'Saya tertarik pada pengembangan metode pengajaran inovatif, modul ajar, dan manajemen pendidikan sekolah.', 'Pendidikan', 18),
        ]

        for kode, teks, kelompok, urutan in questions_data:
            InterestQuestion.objects.update_or_create(
                kode_pertanyaan=kode,
                defaults={
                    'teks_pertanyaan': teks,
                    'kelompok_minat': kelompok,
                    'urutan': urutan,
                    'is_active': True,
                    'skala_minimum': 1,
                    'skala_maksimum': 5,
                }
            )
        self.stdout.write(self.style.SUCCESS(f"Berhasil menginisialisasi {len(questions_data)} pertanyaan instrumen minat & bakat."))

        # 3. Seed Dataset Latih Alumni MA Plus Peradaban Insani (120 records)
        major_templates = {
            'Teknik Informatika': {
                'mtk': (85, 96), 'bind': (75, 88), 'bing': (82, 95), 'ipa': (82, 92), 'ips': (70, 80), 'agama': (78, 88),
                'minat_tek': (4.2, 5.0), 'minat_sai': (3.2, 4.3), 'minat_bis': (2.8, 3.8), 'minat_sos': (2.0, 3.2), 'minat_sen': (3.0, 4.2), 'minat_pen': (2.2, 3.4)
            },
            'Sistem Informasi': {
                'mtk': (80, 92), 'bind': (78, 90), 'bing': (80, 92), 'ipa': (75, 85), 'ips': (78, 90), 'agama': (78, 88),
                'minat_tek': (4.0, 4.8), 'minat_sai': (2.8, 3.8), 'minat_bis': (4.0, 4.9), 'minat_sos': (3.0, 4.0), 'minat_sen': (2.8, 3.8), 'minat_pen': (2.5, 3.5)
            },
            'Kedokteran': {
                'mtk': (88, 98), 'bind': (82, 92), 'bing': (85, 96), 'ipa': (90, 99), 'ips': (72, 82), 'agama': (82, 92),
                'minat_tek': (2.8, 3.8), 'minat_sai': (4.5, 5.0), 'minat_bis': (2.2, 3.2), 'minat_sos': (3.2, 4.2), 'minat_sen': (2.0, 3.0), 'minat_pen': (2.8, 3.8)
            },
            'Farmasi': {
                'mtk': (84, 94), 'bind': (80, 90), 'bing': (80, 92), 'ipa': (88, 98), 'ips': (70, 80), 'agama': (80, 90),
                'minat_tek': (2.5, 3.5), 'minat_sai': (4.3, 5.0), 'minat_bis': (3.0, 4.0), 'minat_sos': (2.2, 3.2), 'minat_sen': (2.0, 3.0), 'minat_pen': (2.5, 3.5)
            },
            'Manajemen Bisnis': {
                'mtk': (76, 88), 'bind': (80, 92), 'bing': (80, 94), 'ipa': (70, 80), 'ips': (85, 96), 'agama': (78, 88),
                'minat_tek': (2.8, 3.8), 'minat_sai': (2.0, 3.0), 'minat_bis': (4.3, 5.0), 'minat_sos': (3.8, 4.7), 'minat_sen': (2.8, 3.8), 'minat_pen': (2.8, 3.8)
            },
            'Akuntansi': {
                'mtk': (84, 96), 'bind': (80, 90), 'bing': (78, 90), 'ipa': (72, 82), 'ips': (88, 98), 'agama': (80, 90),
                'minat_tek': (3.0, 4.0), 'minat_sai': (2.0, 3.0), 'minat_bis': (4.4, 5.0), 'minat_sos': (3.0, 4.0), 'minat_sen': (2.0, 3.0), 'minat_pen': (2.5, 3.5)
            },
            'Ilmu Hukum': {
                'mtk': (70, 82), 'bind': (85, 96), 'bing': (80, 92), 'ipa': (70, 80), 'ips': (86, 97), 'agama': (82, 92),
                'minat_tek': (2.0, 3.0), 'minat_sai': (2.0, 3.0), 'minat_bis': (3.2, 4.2), 'minat_sos': (4.4, 5.0), 'minat_sen': (2.5, 3.5), 'minat_pen': (3.0, 4.0)
            },
            'Psikologi': {
                'mtk': (74, 86), 'bind': (84, 95), 'bing': (82, 94), 'ipa': (78, 88), 'ips': (84, 95), 'agama': (82, 92),
                'minat_tek': (2.2, 3.2), 'minat_sai': (3.4, 4.4), 'minat_bis': (2.8, 3.8), 'minat_sos': (4.3, 5.0), 'minat_sen': (3.0, 4.0), 'minat_pen': (3.4, 4.4)
            },
            'Pendidikan Agama Islam': {
                'mtk': (72, 84), 'bind': (82, 94), 'bing': (75, 88), 'ipa': (70, 82), 'ips': (80, 92), 'agama': (90, 99),
                'minat_tek': (2.0, 3.0), 'minat_sai': (2.0, 3.0), 'minat_bis': (2.5, 3.5), 'minat_sos': (3.5, 4.5), 'minat_sen': (2.8, 3.8), 'minat_pen': (4.5, 5.0)
            },
            'Desain Komunikasi Visual': {
                'mtk': (70, 82), 'bind': (80, 90), 'bing': (80, 92), 'ipa': (70, 80), 'ips': (75, 86), 'agama': (78, 88),
                'minat_tek': (3.5, 4.5), 'minat_sai': (2.0, 3.0), 'minat_bis': (3.0, 4.0), 'minat_sos': (2.8, 3.8), 'minat_sen': (4.5, 5.0), 'minat_pen': (2.5, 3.5)
            },
        }

        # Bersihkan data latih lama jika ada
        TrainingRecord.objects.all().delete()
        random.seed(42)

        records_to_create = []
        for major, tpl in major_templates.items():
            # Buat 12 data latih untuk setiap 10 jurusan (total 120 data latih seimbang)
            for _ in range(12):
                mtk = round(random.uniform(*tpl['mtk']), 1)
                bind = round(random.uniform(*tpl['bind']), 1)
                bing = round(random.uniform(*tpl['bing']), 1)
                ipa = round(random.uniform(*tpl['ipa']), 1)
                ips = round(random.uniform(*tpl['ips']), 1)
                agama = round(random.uniform(*tpl['agama']), 1)

                m_tek = round(random.uniform(*tpl['minat_tek']), 2)
                m_sai = round(random.uniform(*tpl['minat_sai']), 2)
                m_bis = round(random.uniform(*tpl['minat_bis']), 2)
                m_sos = round(random.uniform(*tpl['minat_sos']), 2)
                m_sen = round(random.uniform(*tpl['minat_sen']), 2)
                m_pen = round(random.uniform(*tpl['minat_pen']), 2)

                feat_dict = {
                    'nilai_matematika': mtk,
                    'nilai_bahasa_indonesia': bind,
                    'nilai_bahasa_inggris': bing,
                    'nilai_ipa': ipa,
                    'nilai_ips': ips,
                    'nilai_agama': agama,
                    'minat_teknologi': m_tek,
                    'minat_sains': m_sai,
                    'minat_bisnis': m_bis,
                    'minat_sosial': m_sos,
                    'minat_seni': m_sen,
                    'minat_pendidikan': m_pen,
                }

                records_to_create.append(
                    TrainingRecord(
                        feature_values=feat_dict,
                        major_label=major,
                        dataset_version='v1.0',
                        source_info='Alumni MA Plus Peradaban Insani (2020-2023)'
                    )
                )

        TrainingRecord.objects.bulk_create(records_to_create)
        self.stdout.write(self.style.SUCCESS(f"Berhasil men-generate {len(records_to_create)} data latih historis alumni (10 jurusan target)."))

        # 4. Latih Model Random Forest Pertama
        success, msg, model_ver = train_random_forest_model(
            n_estimators=100,
            max_depth=None,
            test_size=0.2,
            random_state=42
        )
        if success:
            self.stdout.write(self.style.SUCCESS(f"Model Random Forest berhasil dilatih: {msg}"))
        else:
            self.stdout.write(self.style.WARNING(f"Pelatihan model awal tertunda: {msg}"))

        # 5. Seed Contoh Siswa dengan Berbagai Status Alur
        # Siswa 1: Ahmad Fauzi (Lengkap & sudah diprediksi 'Berhasil')
        s1, _ = Student.objects.update_or_create(
            nis='2024001',
            defaults={
                'nama': 'Ahmad Fauzi',
                'kelas': 'XII IPA 1',
                'tahun_ajaran': '2024/2025',
                'status_pengisian': 'Sudah mengisi',
                'status_prediksi': 'Berhasil'
            }
        )
        StudentAcademicData.objects.update_or_create(
            student=s1,
            defaults={
                'nilai_matematika': 92.5,
                'nilai_bahasa_indonesia': 85.0,
                'nilai_bahasa_inggris': 88.0,
                'nilai_ipa': 89.0,
                'nilai_ips': 75.0,
                'nilai_agama': 85.0,
            }
        )
        # Jawaban minat s1 (Condong ke Teknologi & Komputer)
        for q in InterestQuestion.objects.all():
            val = 5 if q.kelompok_minat == 'Teknologi & Komputer' else (4 if q.kelompok_minat == 'Sains & Kesehatan' else 2)
            StudentInterestResponse.objects.update_or_create(student=s1, question=q, defaults={'answer_value': val})

        # Jalankan prediksi untuk Siswa 1 agar hasil rekomendasi langsung siap dibuka
        if model_ver:
            predict_for_student(s1, model_ver)

        # Siswa 2: Siti Nurhaliza (Lengkap, menunggu prediksi Admin)
        s2, _ = Student.objects.update_or_create(
            nis='2024002',
            defaults={
                'nama': 'Siti Nurhaliza',
                'kelas': 'XII IPA 1',
                'tahun_ajaran': '2024/2025',
                'status_pengisian': 'Sudah mengisi',
                'status_prediksi': 'Menunggu'
            }
        )
        StudentAcademicData.objects.update_or_create(
            student=s2,
            defaults={
                'nilai_matematika': 94.0,
                'nilai_bahasa_indonesia': 88.0,
                'nilai_bahasa_inggris': 90.0,
                'nilai_ipa': 96.0,
                'nilai_ips': 78.0,
                'nilai_agama': 88.0,
            }
        )
        for q in InterestQuestion.objects.all():
            val = 5 if q.kelompok_minat == 'Sains & Kesehatan' else (3 if q.kelompok_minat == 'Teknologi & Komputer' else 2)
            StudentInterestResponse.objects.update_or_create(student=s2, question=q, defaults={'answer_value': val})

        # Siswa 3: Muhammad Rizky (Punya nilai akademik, belum mengisi formulir)
        s3, _ = Student.objects.update_or_create(
            nis='2024003',
            defaults={
                'nama': 'Muhammad Rizky Pratama',
                'kelas': 'XII IPS 1',
                'tahun_ajaran': '2024/2025',
                'status_pengisian': 'Belum mengisi',
                'status_prediksi': 'Menunggu'
            }
        )
        StudentAcademicData.objects.update_or_create(
            student=s3,
            defaults={
                'nilai_matematika': 82.0,
                'nilai_bahasa_indonesia': 86.0,
                'nilai_bahasa_inggris': 84.0,
                'nilai_ipa': 75.0,
                'nilai_ips': 92.0,
                'nilai_agama': 85.0,
            }
        )

        # Siswa 4: Aisyah Zahra (Nilai lengkap, sudah isi, status 'Perlu prediksi ulang')
        s4, _ = Student.objects.update_or_create(
            nis='2024004',
            defaults={
                'nama': 'Aisyah Zahra Maulida',
                'kelas': 'XII Keagamaan',
                'tahun_ajaran': '2024/2025',
                'status_pengisian': 'Sudah mengisi',
                'status_prediksi': 'Perlu prediksi ulang'
            }
        )
        StudentAcademicData.objects.update_or_create(
            student=s4,
            defaults={
                'nilai_matematika': 78.0,
                'nilai_bahasa_indonesia': 88.0,
                'nilai_bahasa_inggris': 82.0,
                'nilai_ipa': 76.0,
                'nilai_ips': 86.0,
                'nilai_agama': 96.0,
            }
        )
        for q in InterestQuestion.objects.all():
            val = 5 if q.kelompok_minat == 'Pendidikan' else (4 if q.kelompok_minat == 'Sosial & Hukum' else 3)
            StudentInterestResponse.objects.update_or_create(student=s4, question=q, defaults={'answer_value': val})

        # Siswa 5: Budi Santoso (Siswa baru, nilai belum lengkap)
        s5, _ = Student.objects.update_or_create(
            nis='2024005',
            defaults={
                'nama': 'Budi Santoso',
                'kelas': 'XII IPS 2',
                'tahun_ajaran': '2024/2025',
                'status_pengisian': 'Belum mengisi',
                'status_prediksi': 'Menunggu'
            }
        )
        StudentAcademicData.objects.update_or_create(
            student=s5,
            defaults={
                'nilai_matematika': 0.0,
                'nilai_bahasa_indonesia': 0.0,
                'nilai_bahasa_inggris': 0.0,
                'nilai_ipa': 0.0,
                'nilai_ips': 0.0,
                'nilai_agama': 0.0,
            }
        )

        self.stdout.write(self.style.SUCCESS("Berhasil membuat 5 contoh siswa dengan berbagai skenario alur."))
        self.stdout.write(self.style.SUCCESS("Seeding SPK selesai! Semua konfigurasi sesuai PRD siap digunakan."))
