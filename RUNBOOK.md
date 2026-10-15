# PRODUCT REQUIREMENTS DOCUMENT (PRD)
## Sistem Rekomendasi Jurusan Kuliah Menggunakan Algoritma Random Forest

**Studi Kasus:** MA Plus Peradaban Insani  
**Platform:** Web Application  
**Backend:** Python dan Django  
**Machine Learning:** Scikit-learn — Random Forest Classifier  
**Database:** SQLite untuk pengembangan awal; dapat disesuaikan dengan kebutuhan deployment  
**Frontend:** HTML, TailwindCSS, dan JavaScript  
**Versi dokumen:** 1.0

---

# 1. Ringkasan Produk

## 1.1 Nama Produk

Sistem Rekomendasi Jurusan Kuliah Berbasis Machine Learning Menggunakan Algoritma Random Forest.

## 1.2 Deskripsi Produk

Aplikasi web ini dirancang untuk membantu siswa MA Plus Peradaban Insani memperoleh rekomendasi jurusan perguruan tinggi berdasarkan data akademik, minat, dan bakat atau kemampuan pendukung yang tersedia.

Sistem menggunakan algoritma Random Forest untuk mempelajari pola dari dataset berlabel, kemudian menghasilkan prediksi jurusan dan mengurutkan maksimal lima jurusan berdasarkan skor probabilitas model.

Aplikasi memiliki dua role pengguna:

1. **Admin:** mengelola data siswa, dataset pelatihan, dan proses prediksi.
2. **Siswa:** melakukan verifikasi NIS, mengisi formulir minat dan bakat, menunggu proses prediksi, serta melihat hasil rekomendasi setelah tersedia.

Admin memiliki tepat lima menu sidebar: Dashboard, Data Siswa, Prediksi Jurusan, Data Latih, dan Logout.

## 1.3 Latar Belakang

Siswa dapat mengalami kesulitan dalam memilih jurusan perguruan tinggi yang sesuai dengan kemampuan akademik dan minatnya. Proses pemilihan yang hanya mengandalkan intuisi berpotensi menghasilkan keputusan yang kurang terarah.

Melalui aplikasi ini, data akademik dan minat siswa dapat diolah menggunakan machine learning untuk menghasilkan rekomendasi yang lebih terstruktur dan dapat dievaluasi.

Sistem berfungsi sebagai alat bantu pengambilan keputusan, bukan sebagai penentu mutlak masa depan pendidikan siswa.

---

# 2. Tujuan Produk

1. Membantu siswa memperoleh rekomendasi jurusan berdasarkan data akademik dan minat.
2. Menyediakan formulir digital untuk pengumpulan data minat dan bakat siswa.
3. Memudahkan admin mengelola data siswa dan dataset pelatihan.
4. Mengimplementasikan algoritma Random Forest untuk prediksi jurusan.
5. Menampilkan proses perhitungan dan hasil prediksi secara transparan.
6. Menampilkan maksimal lima jurusan teratas berdasarkan skor prediksi model.
7. Menyediakan hasil yang dapat ditelusuri berdasarkan siswa, waktu prediksi, dan versi model.

## 2.1 Indikator Keberhasilan

- Siswa dapat menyelesaikan proses cek NIS dan pengisian formulir.
- Admin dapat mengelola data siswa dan data latih melalui operasi CRUD.
- Sistem dapat melatih dan mengevaluasi model menggunakan dataset yang valid.
- Admin dapat menjalankan prediksi untuk siswa dengan data lengkap.
- Sistem menampilkan detail proses dan maksimal lima rekomendasi jurusan.
- Siswa hanya dapat melihat hasil miliknya sendiri.
- Hasil prediksi yang gagal tidak dipublikasikan sebagai hasil berhasil.

---

# 3. Ruang Lingkup Produk

## 3.1 Fitur yang Termasuk MVP

- Autentikasi dan otorisasi dua role.
- Pengecekan NIS siswa.
- Formulir minat dan bakat.
- Penyimpanan dan validasi data siswa.
- Dashboard admin.
- CRUD data siswa.
- CRUD dataset pelatihan.
- Preprocessing dan pelatihan Random Forest.
- Evaluasi model.
- Prediksi jurusan oleh admin.
- Tampilan detail proses prediksi.
- Peringkat maksimal lima rekomendasi.
- Status menunggu, diproses, berhasil, dan gagal.
- Halaman hasil rekomendasi siswa.
- Logout dan pembatasan akses.

## 3.2 Di Luar Ruang Lingkup

- Aplikasi mobile native.
- Integrasi langsung dengan sistem penerimaan mahasiswa baru.
- Rekomendasi berdasarkan kuota atau peluang lolos seleksi kampus.
- Chatbot konsultasi.
- Tes psikologi profesional.
- Prediksi keberhasilan siswa setelah memasuki perguruan tinggi.
- Penentuan jurusan secara otomatis tanpa pengawasan admin.
- Multi-role Guru BK tersendiri.

---

# 4. Role dan Hak Akses

Aplikasi hanya memiliki dua role.

## 4.1 Admin

Admin bertanggung jawab atas pengelolaan data dan pelaksanaan proses machine learning.

Hak akses:

- Melihat dashboard.
- Menambah, melihat, mengubah, dan menghapus data siswa.
- Memeriksa nilai rapor serta jawaban minat dan bakat.
- Mengelola data latih.
- Menjalankan proses pelatihan dan evaluasi model melalui bagian pengelolaan data latih.
- Memilih siswa yang akan diprediksi.
- Melihat detail proses perhitungan.
- Melihat hasil rekomendasi seluruh siswa.
- Mempublikasikan hasil setelah prediksi berhasil.
- Melihat riwayat hasil prediksi.

## 4.2 Siswa

Siswa tidak memiliki akses ke dashboard atau menu admin.

Hak akses:

- Memasukkan NIS untuk verifikasi.
- Mengisi formulir minat dan bakat.
- Mengirim jawaban.
- Melihat status pengajuan.
- Melihat hasil rekomendasi miliknya setelah prediksi berhasil.

Siswa tidak boleh mengubah nilai rapor, mengelola dataset, menjalankan model, atau melihat data siswa lain.

---

# 5. Struktur Navigasi

## 5.1 Sidebar Admin

Sidebar admin hanya terdiri dari lima menu berikut.

### 1. Dashboard

Menampilkan ringkasan sistem.

### 2. Data Siswa

Mengelola data siswa, nilai rapor, dan status pengisian formulir.

### 3. Prediksi Jurusan

Memilih siswa, menjalankan prediksi, memeriksa proses perhitungan, dan melihat hasil rekomendasi.

### 4. Data Latih

Mengelola dataset, atribut, label, serta proses pelatihan dan evaluasi model.

### 5. Logout

Mengakhiri sesi admin dengan aman.

**Ketentuan:** evaluasi model, preprocessing, detail perhitungan, dan riwayat prediksi menjadi bagian dari halaman atau subhalaman yang relevan. Fitur tersebut tidak menambahkan item baru pada sidebar.

## 5.2 Navigasi Siswa

Siswa menggunakan halaman terpisah tanpa sidebar admin:

1. Halaman cek NIS.
2. Formulir minat dan bakat.
3. Halaman konfirmasi pengiriman.
4. Halaman status menunggu prediksi.
5. Halaman hasil rekomendasi.

---

# 6. Kebutuhan Fungsional

## FR-01 — Autentikasi dan Otorisasi

- Sistem harus membedakan akses admin dan siswa.
- Admin masuk melalui halaman login.
- Siswa menggunakan proses cek NIS untuk menemukan data yang sesuai.
- Sistem membatasi halaman berdasarkan role.
- Siswa tidak boleh mengakses URL admin secara langsung.
- Logout mengakhiri sesi pengguna.

**Catatan keamanan:** NIS saja bukan autentikasi yang kuat. Sebaiknya siswa melakukan verifikasi tambahan atau menggunakan mekanisme akses yang sesuai agar orang lain tidak dapat mengambil hasil siswa hanya dengan mengetahui NIS-nya.

## FR-02 — Dashboard Admin

Dashboard menampilkan:

- Total siswa terdaftar.
- Jumlah siswa yang sudah mengisi formulir.
- Jumlah siswa yang menunggu prediksi.
- Jumlah prediksi berhasil.
- Jumlah prediksi gagal.
- Jumlah data latih.
- Status model yang tersedia.
- Ringkasan jurusan yang paling sering direkomendasikan.

Data dashboard diambil dari database dan hasil prediksi aktual.

## FR-03 — Data Siswa (CRUD)

Admin dapat:

- Menambah siswa.
- Melihat daftar siswa.
- Melihat detail siswa.
- Mengubah data siswa.
- Menghapus data siswa.
- Mencari berdasarkan NIS atau nama.
- Memfilter berdasarkan status pengisian dan prediksi.
- Memasukkan atau memperbarui nilai rapor.
- Melihat jawaban formulir minat dan bakat.

Validasi:

- NIS harus unik.
- Nilai harus sesuai rentang yang ditentukan.
- Data wajib tidak boleh kosong.
- Data yang sudah memiliki riwayat prediksi harus ditangani dengan aturan penghapusan yang menjaga integritas riwayat.

## FR-04 — Formulir Minat dan Bakat Siswa

Setelah NIS berhasil diverifikasi, sistem menampilkan formulir sesuai data yang dibutuhkan model.

Formulir dapat memuat:

- Minat terhadap bidang studi.
- Minat terhadap aktivitas atau bidang pekerjaan.
- Pertanyaan kemampuan atau bakat yang memiliki dasar instrumen yang jelas.
- Pertanyaan pendukung lain yang telah ditentukan dalam rancangan penelitian.

Kebutuhan:

- Pertanyaan memiliki pilihan jawaban atau skala yang konsisten.
- Skala dan pengkodean jawaban ditetapkan sebelum model digunakan.
- Jawaban tersimpan berdasarkan identitas siswa.
- Sistem memvalidasi jawaban wajib.
- Siswa memperoleh konfirmasi setelah pengiriman.
- Jawaban tidak langsung menghasilkan rekomendasi sebelum admin menjalankan prediksi.

Jika bakat tidak memiliki instrumen yang valid atau data yang memadai, sistem harus menghindari penyebutan skor sebagai hasil tes bakat profesional.

## FR-05 — Pengelolaan Status Siswa

Setiap siswa memiliki status pengisian dan status prediksi.

Status pengisian:

- Belum mengisi.
- Sudah mengisi.
- Perlu melengkapi data.

Status prediksi:

- Menunggu.
- Diproses.
- Berhasil.
- Gagal.
- Perlu prediksi ulang.

Status pengisian dan status prediksi disimpan terpisah agar sistem dapat membedakan siswa yang belum mengirim formulir dengan siswa yang sudah siap diprediksi.

## FR-06 — Data Latih (CRUD)

Admin dapat:

- Menambah data latih.
- Melihat daftar data latih.
- Mengubah data latih.
- Menghapus data latih.
- Mengimpor data dari CSV atau Excel.
- Memeriksa kolom dan tipe data.
- Memeriksa nilai kosong dan data duplikat.
- Memeriksa label jurusan.
- Melihat jumlah data pada masing-masing kelas.
- Menjalankan preprocessing, pelatihan, dan evaluasi model dari halaman ini.

Dataset pelatihan wajib mempunyai label jurusan yang jelas. Data siswa yang belum memiliki label tidak otomatis menjadi data pelatihan berlabel.

Perubahan dataset setelah model dilatih harus ditandai agar admin mengetahui bahwa model yang tersimpan mungkin belum menggunakan dataset terbaru.

## FR-07 — Pelatihan Model Random Forest

Sistem harus mendukung pelatihan Random Forest menggunakan Scikit-learn.

Proses mencakup:

1. Memvalidasi dataset.
2. Menentukan fitur dan label.
3. Memisahkan data latih dan data uji.
4. Melakukan preprocessing sesuai tipe fitur.
5. Melatih Random Forest.
6. Menyimpan model dan preprocessing pipeline.
7. Menyimpan parameter dan versi model.
8. Menampilkan status pelatihan.

Parameter model, seperti jumlah pohon, kedalaman maksimum, dan random seed, dicatat agar eksperimen dapat direproduksi.

Sistem tidak boleh mengklaim model sudah siap jika pelatihan gagal atau dataset tidak memenuhi persyaratan.

## FR-08 — Evaluasi Model

Sistem menampilkan hasil evaluasi dari data uji yang tidak digunakan untuk melatih model tersebut.

Metrik meliputi:

- Accuracy.
- Precision.
- Recall.
- F1-score.
- Confusion matrix.

Jika terdapat beberapa kelas jurusan, precision, recall, dan F1-score perlu dijelaskan menggunakan skema averaging yang sesuai, misalnya macro atau weighted.

Nilai metrik harus berasal dari perhitungan aktual, bukan angka yang ditentukan sebagai target atau diisi manual.

## FR-09 — Prediksi Jurusan

Halaman Prediksi Jurusan menyediakan:

- Daftar siswa yang datanya siap diprediksi.
- Pencarian berdasarkan NIS atau nama.
- Filter status prediksi.
- Pemilihan satu siswa atau beberapa siswa.
- Tombol **Prediksi**.
- Status proses.
- Tautan atau panel untuk melihat detail perhitungan.
- Hasil rekomendasi setelah proses berhasil.

Sebelum prediksi dijalankan, sistem memeriksa:

- Data akademik lengkap.
- Formulir minat dan bakat sudah dikirim.
- Fitur yang diperlukan tersedia.
- Model yang kompatibel sudah dilatih.
- Data dapat diproses oleh pipeline yang tersimpan.

Jika validasi gagal, sistem menampilkan alasan yang dapat ditindaklanjuti.

## FR-10 — Detail Perhitungan Prediksi

Setelah admin menjalankan prediksi, sistem menampilkan tahapan berikut.

### Tahap 1 — Data input

Menampilkan fitur yang benar-benar dipakai model, misalnya:

- Nilai mata pelajaran.
- Skor minat.
- Skor kemampuan pendukung jika tersedia.

Identitas seperti NIS hanya digunakan untuk pencarian dan pengaitan hasil, bukan sebagai fitur model.

### Tahap 2 — Validasi dan preprocessing

Menampilkan:

- Status kelengkapan data.
- Nilai sebelum transformasi.
- Transformasi atau encoding yang dilakukan.
- Nilai fitur akhir yang diterima model.

Jika model tidak memerlukan normalisasi, sistem tidak boleh menampilkan seolah-olah normalisasi telah dilakukan.

### Tahap 3 — Informasi model

Menampilkan:

- Algoritma: Random Forest Classifier.
- Versi model.
- Tanggal pelatihan.
- Jumlah pohon keputusan.
- Parameter penting yang digunakan.
- Dataset atau versi dataset pelatihan.

### Tahap 4 — Proses prediksi

Menampilkan ringkasan proses yang benar-benar dapat diperoleh dari implementasi, seperti:

- Hasil kelas dari model.
- Distribusi probabilitas tiap kelas jika tersedia.
- Ringkasan suara pohon jika mekanisme tersebut direkam.
- Feature importance global dari model, bila dihitung.

Sistem tidak wajib menampilkan seluruh struktur setiap pohon keputusan. Tampilan proses harus tetap sesuai dengan hasil yang benar-benar dihitung.

### Tahap 5 — Pengurutan rekomendasi

- Mengambil skor untuk setiap kelas jurusan.
- Mengurutkan skor dari terbesar ke terkecil.
- Memilih maksimal lima jurusan.
- Menetapkan peringkat pertama sebagai rekomendasi utama.

### Tahap 6 — Penyimpanan hasil

Menyimpan:

- Siswa yang diprediksi.
- Fitur atau referensi data yang digunakan.
- Hasil prediksi.
- Skor per jurusan.
- Peringkat.
- Waktu prediksi.
- Versi model.
- Status proses.

Hasil hanya boleh dipublikasikan setelah penyimpanan berhasil.

## FR-11 — Hasil Rekomendasi Lima Jurusan Teratas

Sistem menampilkan maksimal lima jurusan dengan skor tertinggi.

Contoh tampilan ilustratif:

| Peringkat | Jurusan | Skor ilustratif |
|---:|---|---:|
| 1 | Teknik Informatika | 85% |
| 2 | Sistem Informasi | 78% |
| 3 | Statistika | 71% |
| 4 | Ekonomi | 64% |
| 5 | Pendidikan | 52% |

Angka tersebut hanya contoh antarmuka, bukan hasil model aktual.

Aturan:

- Nama jurusan dan skor diambil dari hasil model.
- Jika tersedia kurang dari lima kelas, tampilkan seluruh kelas yang tersedia.
- Skor harus diurutkan menurun.
- Rekomendasi utama ditandai dengan jelas.
- Skor probabilitas tidak boleh disebut sebagai jaminan kecocokan atau keberhasilan.
- Hasil dapat dilihat admin dan siswa pemilik hasil sesuai hak akses.

## FR-12 — Publikasi Hasil kepada Siswa

Sebelum prediksi berhasil, siswa melihat status menunggu atau diproses.

Setelah prediksi berhasil dan hasil tersimpan:

- Status berubah menjadi berhasil.
- Halaman hasil siswa tersedia.
- Siswa dapat melihat peringkat maksimal lima jurusan dan skor.
- Siswa tidak dapat melihat hasil siswa lain.

Jika prediksi gagal, hasil baru tidak dipublikasikan sebagai hasil sukses.

Jika jawaban siswa berubah setelah prediksi, hasil sebelumnya ditandai perlu diperbarui dan admin harus menjalankan prediksi ulang sebelum hasil terbaru dipublikasikan.

## FR-13 — Riwayat Prediksi

Riwayat prediksi merupakan bagian dari halaman Prediksi Jurusan, bukan menu sidebar tersendiri.

Admin dapat melihat:

- Siswa yang diprediksi.
- Waktu proses.
- Status proses.
- Model yang digunakan.
- Hasil rekomendasi.
- Kesalahan yang terjadi jika proses gagal.

Riwayat lama sebaiknya dipertahankan agar hasil terdahulu dapat ditelusuri.

---

# 7. Alur Penggunaan Sistem

## 7.1 Alur Siswa

1. Siswa membuka halaman cek NIS.
2. Siswa memasukkan NIS.
3. Sistem memvalidasi data dan akses.
4. Siswa mengisi formulir minat dan bakat.
5. Siswa mengirim jawaban.
6. Sistem menyimpan jawaban dan menampilkan konfirmasi.
7. Siswa melihat status menunggu prediksi.
8. Admin menjalankan prediksi.
9. Setelah berhasil, sistem menyediakan halaman hasil.
10. Siswa membuka hasil rekomendasi dan melihat lima jurusan teratas.

## 7.2 Alur Admin

1. Admin login.
2. Admin membuka Dashboard.
3. Admin mengelola Data Siswa.
4. Admin membuka Data Latih.
5. Admin memvalidasi dataset, melatih model, dan memeriksa evaluasi.
6. Admin membuka Prediksi Jurusan.
7. Admin memilih siswa yang sudah lengkap datanya.
8. Admin menekan Prediksi.
9. Sistem melakukan validasi, preprocessing, dan prediksi.
10. Sistem menampilkan detail proses dan skor jurusan.
11. Sistem menyimpan hasil serta versi model.
12. Sistem menyediakan hasil bagi siswa terkait.

---

# 8. Rancangan Database

Entitas berikut merupakan rancangan awal untuk implementasi Django.

## 8.1 User

Menyimpan akun admin dan, jika dibutuhkan, akun siswa.

Atribut utama:

- id
- username
- password_hash
- role
- is_active
- created_at

Gunakan sistem autentikasi Django dan penyimpanan password yang aman. Jangan menyimpan password dalam bentuk teks biasa.

## 8.2 Student

Menyimpan identitas siswa.

- id
- nis
- nama
- kelas
- tahun_ajaran
- created_at
- updated_at

NIS harus unik.

## 8.3 StudentAcademicData

Menyimpan nilai akademik.

- id
- student_id
- nilai_matematika
- nilai_bahasa_inggris
- nilai_bahasa_indonesia
- nilai_mata_pelajaran_lain
- updated_at

Kolom nilai disesuaikan dengan mata pelajaran dan data yang benar-benar tersedia. Nilai tidak boleh diisi dengan contoh atau perkiraan tanpa sumber.

## 8.4 InterestQuestion

Menyimpan definisi pertanyaan.

- id
- kode_pertanyaan
- teks_pertanyaan
- kelompok_minat
- tipe_jawaban
- skala_minimum
- skala_maksimum
- is_active

## 8.5 StudentInterestResponse

Menyimpan jawaban kuesioner.

- id
- student_id
- question_id
- answer_value
- submitted_at

Sistem harus dapat mengidentifikasi versi formulir atau instrumen yang digunakan.

## 8.6 TrainingRecord

Menyimpan data pelatihan.

- id
- feature_values
- major_label
- dataset_version
- created_at

Struktur fitur sebaiknya memiliki skema yang konsisten. Untuk implementasi produksi, kolom terstruktur atau tabel relasional lebih mudah divalidasi daripada menyimpan semua data tanpa struktur.

## 8.7 ModelVersion

Menyimpan metadata model.

- id
- version_name
- algorithm
- parameters
- dataset_version
- evaluation_metrics
- artifact_path
- trained_at
- status

Artifact model harus disimpan pada lokasi yang aman dan hanya dimuat dari sumber yang dipercaya.

## 8.8 PredictionRun

Mencatat proses prediksi.

- id
- student_id
- model_version_id
- status
- input_snapshot
- started_at
- completed_at
- error_message

## 8.9 RecommendationResult

Menyimpan hasil per jurusan.

- id
- prediction_run_id
- major_label
- score
- rank

Satu proses prediksi dapat memiliki beberapa baris hasil rekomendasi, sesuai jumlah kelas yang diprediksi.

---

# 9. Arsitektur Teknologi

## 9.1 Backend

**Python dan Django**

Tanggung jawab:

- Autentikasi dan otorisasi.
- CRUD data siswa dan data latih.
- Validasi formulir.
- Pengelolaan status prediksi.
- Integrasi dengan model machine learning.
- Penyimpanan dan publikasi hasil.

## 9.2 Machine Learning

**Scikit-learn**

Komponen:

- RandomForestClassifier.
- Pipeline preprocessing jika diperlukan.
- Pemisahan data latih dan uji.
- Evaluasi classification metrics.
- Prediksi kelas dan probabilitas.
- Penyimpanan model beserta preprocessing yang sesuai.

**Penting:** model dan preprocessing harus berasal dari pipeline pelatihan yang kompatibel. Jangan melatih ulang model setiap kali siswa meminta hasil.

## 9.3 Frontend

- HTML.
- CSS.
- Bootstrap.
- JavaScript seperlunya.

Desain harus responsif untuk laptop, tablet, dan ponsel.

## 9.4 Database

SQLite dapat digunakan selama pengembangan dan pengujian awal. Database dapat diganti dengan PostgreSQL atau MySQL apabila diperlukan oleh lingkungan deployment.

---

# 10. Ketentuan Metodologi Machine Learning

Bagian ini penting agar implementasi aplikasi konsisten dengan penelitian skripsi.

## 10.1 Fitur

Fitur awal dapat mencakup:

- Nilai rapor.
- Skor minat.
- Skor kemampuan pendukung jika tersedia dan terukur.

Fitur final ditentukan berdasarkan sumber data sekolah, instrumen yang digunakan, dataset, dan tujuan penelitian.

## 10.2 Label

Label merupakan kelas jurusan yang digunakan model saat pelatihan.

Sumber label harus dipastikan sebelum implementasi final, misalnya program studi yang dipilih atau dimasuki alumni, atau label lain yang benar-benar tersedia dan relevan dengan tujuan penelitian.

Sistem tidak boleh membuat label pelatihan hanya berdasarkan asumsi admin tanpa prosedur yang terdokumentasi.

## 10.3 Pembobotan

Random Forest tidak mensyaratkan pembobotan manual atribut seperti:

- Nilai rapor 60%.
- Minat siswa 40%.

Model mempelajari pola dari data pelatihan. Jika penelitian menggunakan bobot manual, dasar metode dan tahap penggunaannya harus dijelaskan secara terpisah.

Feature importance dapat membantu menjelaskan kontribusi fitur pada model secara global, tetapi bukan persentase kecocokan setiap siswa.

## 10.4 Skor Jurusan

Gunakan probabilitas kelas yang dihasilkan model jika `predict_proba()` tersedia dan sesuai dengan model yang dilatih.

Skor yang ditampilkan:

- Berasal dari hasil perhitungan aktual.
- Diurutkan dari terbesar ke terkecil.
- Dijelaskan sebagai probabilitas prediksi model.
- Tidak diklaim sebagai jaminan keberhasilan akademik atau ukuran psikologis yang pasti.

## 10.5 Evaluasi

Model dievaluasi menggunakan data uji yang terpisah dari data pelatihan. Proses preprocessing dan pemilihan fitur harus menghindari data leakage.

Jika kelas jurusan tidak seimbang, laporan evaluasi perlu mencakup metrik per kelas atau macro-F1 selain accuracy.

---

# 11. Kebutuhan Nonfungsional

## 11.1 Keamanan

- Gunakan proteksi CSRF Django untuk formulir yang sesuai.
- Terapkan pemeriksaan role pada setiap endpoint dan halaman.
- Batasi akses hasil berdasarkan kepemilikan siswa.
- Validasi data pada server.
- Lindungi kredensial dan file model.
- Jangan menampilkan data pribadi yang tidak dibutuhkan.
- Catat tindakan admin yang penting.

## 11.2 Kinerja

- Halaman CRUD harus tetap responsif untuk volume data sekolah.
- Proses prediksi harus memberikan status yang jelas.
- Prediksi banyak siswa dapat dijalankan dalam batch jika volume data membutuhkannya.
- Jika proses panjang, gunakan mekanisme background task yang sesuai; jangan menampilkan status berhasil sebelum proses selesai.

## 11.3 Usabilitas

- Bahasa antarmuka menggunakan Bahasa Indonesia.
- Navigasi sederhana.
- Pesan validasi jelas.
- Tabel mendukung pencarian dan pagination.
- Formulir siswa mudah dipahami.
- Hasil rekomendasi mudah dibaca pada perangkat mobile.

## 11.4 Maintainability

- Pisahkan logika aplikasi Django dari logika machine learning.
- Gunakan pipeline preprocessing dan model yang dapat direproduksi.
- Simpan versi model.
- Buat pengujian otomatis untuk alur utama.
- Dokumentasikan skema fitur dan label.

---

# 12. Kriteria Penerimaan (Acceptance Criteria)

| ID | Kriteria |
|---|---|
| AC-01 | Sistem hanya menyediakan dua role: Admin dan Siswa. |
| AC-02 | Sidebar admin hanya memiliki Dashboard, Data Siswa, Prediksi Jurusan, Data Latih, dan Logout. |
| AC-03 | Siswa dapat melanjutkan ke formulir setelah NIS berhasil diverifikasi. |
| AC-04 | Siswa tidak dapat melihat hasil sebelum prediksi berhasil dan dipublikasikan. |
| AC-05 | Admin dapat melakukan CRUD data siswa. |
| AC-06 | Admin dapat melakukan CRUD data latih. |
| AC-07 | Sistem menolak prediksi jika fitur wajib tidak lengkap atau model belum siap. |
| AC-08 | Sistem menampilkan tahapan proses dan hasil perhitungan yang sesuai dengan implementasi model. |
| AC-09 | Sistem menampilkan maksimal lima jurusan berdasarkan urutan skor tertinggi. |
| AC-10 | Hasil disimpan dengan waktu prediksi dan versi model. |
| AC-11 | Siswa hanya dapat mengakses hasil miliknya sendiri. |
| AC-12 | Jika prediksi gagal, status kegagalan ditampilkan dan hasil gagal tidak dipublikasikan sebagai hasil sukses. |
| AC-13 | Metrik evaluasi dihitung dari hasil pengujian model aktual. |
| AC-14 | Perubahan data atau jawaban setelah prediksi ditangani melalui penandaan perlu prediksi ulang. |

---

# 13. Rencana Pengujian

## 13.1 Pengujian Fungsional

- Login admin.
- Akses halaman berdasarkan role.
- Validasi NIS.
- Pengisian formulir.
- CRUD data siswa.
- CRUD data latih.
- Pelatihan dan evaluasi model.
- Prediksi siswa.
- Penampilan lima rekomendasi.
- Publikasi hasil.
- Logout.

## 13.2 Pengujian Machine Learning

- Dataset dengan nilai kosong.
- Dataset dengan kelas yang tidak seimbang.
- Model belum dilatih.
- Input dengan fitur tidak lengkap.
- Kesesuaian urutan fitur saat inferensi.
- Validitas urutan skor rekomendasi.
- Kesesuaian hasil prediksi dengan keluaran model.
- Evaluasi pada data uji terpisah.

## 13.3 Pengujian Keamanan

- Siswa mencoba mengakses URL admin.
- Siswa mencoba melihat hasil siswa lain.
- Pengiriman NIS yang tidak valid.
- Pengubahan data melalui request langsung.
- Penggunaan sesi setelah logout.

---

# 14. Risiko dan Mitigasi

| Risiko | Mitigasi |
|---|---|
| Dataset pelatihan terlalu sedikit | Audit jumlah data dan jelaskan keterbatasan hasil penelitian. |
| Label jurusan tidak konsisten | Tetapkan sumber label dan kamus kategori sebelum pelatihan. |
| Nilai atau jawaban tidak lengkap | Validasi sebelum prediksi. |
| Skor dianggap sebagai jaminan kecocokan | Jelaskan bahwa skor merupakan probabilitas prediksi model. |
| Model belum diperbarui setelah data latih berubah | Tampilkan versi dataset dan tanggal pelatihan. |
| Siswa mengakses hasil siswa lain | Verifikasi akses dan pembatasan berdasarkan identitas. |
| Hasil prediksi lama masih ditampilkan setelah perubahan data | Tandai hasil perlu prediksi ulang. |
| Admin menganggap feature importance sebagai bobot personal | Jelaskan perbedaan feature importance global dan skor probabilitas individual. |

---

# 15. Keputusan yang Masih Harus Ditetapkan

Sebelum pengembangan dimulai, keputusan berikut perlu dikunci.

1. **Kategori jurusan:** daftar kelas jurusan perguruan tinggi yang akan diprediksi.
2. **Sumber label:** data historis program studi alumni atau sumber label lain yang tersedia.
3. **Atribut final:** daftar nilai rapor, pertanyaan minat, dan atribut kemampuan yang benar-benar tersedia.
4. **Instrumen minat dan bakat:** daftar pertanyaan, skala penilaian, dan cara pengolahan jawaban.
5. **Sumber nilai rapor:** input admin manual atau impor file dari sekolah.
6. **Aturan verifikasi siswa:** apakah cek NIS disertai kode verifikasi atau mekanisme akses tambahan.
7. **Aturan model:** pembagian data, parameter Random Forest, evaluasi, dan versi model.
8. **Publikasi hasil:** apakah prediksi yang selesai langsung tersedia untuk siswa atau harus melalui konfirmasi admin.

Keputusan tersebut tidak boleh diisi dengan asumsi tanpa persetujuan atau data pendukung.

---

# 16. Urutan Implementasi

1. Menyiapkan project Django dan autentikasi dua role.
2. Membuat database dan CRUD Data Siswa.
3. Membuat CRUD Data Latih.
4. Membuat halaman cek NIS dan formulir minat/bakat.
5. Menetapkan skema fitur, label, dan preprocessing.
6. Mengimplementasikan pelatihan serta evaluasi Random Forest.
7. Membuat halaman Prediksi Jurusan.
8. Menampilkan detail proses, skor, dan lima jurusan teratas.
9. Mengimplementasikan status serta publikasi hasil kepada siswa.
10. Melakukan pengujian fungsional, keamanan, dan machine learning.
11. Menyiapkan dokumentasi implementasi untuk mendukung penulisan skripsi.

---

# 17. Kesimpulan

Aplikasi dibangun menggunakan Django dan Random Forest dengan dua role utama. Admin memiliki tepat lima menu sidebar, sedangkan siswa menjalani alur cek NIS, mengisi minat dan bakat, menunggu prediksi, lalu melihat hasil setelah admin menyelesaikan proses.

Fokus utama aplikasi adalah pengelolaan data yang konsisten, prediksi yang dapat ditelusuri, evaluasi model yang benar, serta penyajian maksimal lima rekomendasi berdasarkan skor yang benar-benar dihasilkan model.

Sistem memberikan rekomendasi sebagai bahan pertimbangan pendidikan dan tidak menggantikan keputusan siswa maupun konsultasi dengan pihak sekolah.