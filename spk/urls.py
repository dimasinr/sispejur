from django.urls import path
from spk import views

urlpatterns = [
    # Alur Siswa
    path('', views.cek_nis_view, name='cek_nis'),
    path('formulir-minat/', views.formulir_minat_view, name='formulir_minat'),
    path('status-menunggu/', views.status_menunggu_view, name='status_menunggu'),
    path('hasil-rekomendasi/', views.hasil_rekomendasi_view, name='hasil_rekomendasi'),
    path('siswa-logout/', views.siswa_logout_view, name='siswa_logout'),

    # Autentikasi Admin
    path('admin-spk/login/', views.admin_login_view, name='admin_login'),
    path('admin-spk/logout/', views.admin_logout_view, name='admin_logout'),

    # 5 Menu Sidebar Admin
    # 1. Dashboard
    path('admin-spk/', views.dashboard_view, name='dashboard'),

    # 2. Data Siswa
    path('admin-spk/siswa/', views.data_siswa_view, name='data_siswa'),
    path('admin-spk/siswa/tambah/', views.siswa_create_view, name='siswa_create'),
    path('admin-spk/siswa/<int:pk>/', views.siswa_detail_view, name='siswa_detail'),
    path('admin-spk/siswa/<int:pk>/edit/', views.siswa_edit_view, name='siswa_edit'),
    path('admin-spk/siswa/<int:pk>/hapus/', views.siswa_delete_view, name='siswa_delete'),

    # 3. Prediksi Jurusan (termasuk riwayat & detail perhitungan)
    path('admin-spk/prediksi/', views.prediksi_jurusan_view, name='prediksi_jurusan'),
    path('admin-spk/prediksi/<int:student_id>/jalankan/', views.run_prediction_single_view, name='run_prediction_single'),
    path('admin-spk/prediksi/batch/', views.run_prediction_batch_view, name='run_prediction_batch'),
    path('admin-spk/prediksi/detail/<int:pk>/', views.prediksi_detail_view, name='prediksi_detail'),

    # 4. Data Latih (termasuk pelatihan model & evaluasi)
    path('admin-spk/data-latih/', views.data_latih_view, name='data_latih'),
    path('admin-spk/data-latih/tambah/', views.data_latih_create_view, name='data_latih_create'),
    path('admin-spk/data-latih/<int:pk>/hapus/', views.data_latih_delete_view, name='data_latih_delete'),
    path('admin-spk/data-latih/import-csv/', views.data_latih_import_csv_view, name='data_latih_import_csv'),
    path('admin-spk/data-latih/train/', views.model_train_view, name='model_train'),
]
