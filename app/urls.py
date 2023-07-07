from django.urls import path
from app import views,auth,api


urlpatterns = [
    #  =========================================================================
    #  =                              SISWA VIEW                               =
    #  =========================================================================
    path('dashboard-siswa/', views.dashboard_siswa, name='home-siswa'),
    path('jadwal-piket/', views.jadwal_piket_siswa, name='jadwal-piket-siswa'),
    path('jadwal-pelajaran/', views.jadwal_pelajaran, name='jadwal-pelajaran-siswa'),
    path('list-pengajar', views.list_pengajar, name='list-pengajar-siswa'),
    path('my-profile', views.profile_siswa, name='profile-siswa'),
    path('profile/<str:username_user>', views.profile_user, name='profile-user'),
    path('tugas', views.tugas_siswa, name='tugas-siswa'),
    path('tugas/<str:id_tugas>', views.detail_tugas, name='detail-tugas-siswa'),
    path('ubah-password', views.ganti_password, name='ganti-pas-siswa'),
    path('pengaturan-umum', views.pengaturan_siswa_umum, name='pengaturan-siswa'),
    path('notifikasi', views.notifikasi_siswa, name='notifikasi-siswa'),
    

    path('kas/', views.kas_siswa, name='kas-siswa'),
    path('login', auth.login_user, name='login'),
    

    #  =========================================================================
    #  =                              GURU VIEW                               =
    #  =========================================================================
    path('dashboard-guru/', views.dashboard_guru, name='home-guru'),
    

    # =========================================================================

    path('logout/', auth.logout_view, name='logout'),

    path('api/kas/', api.api_kas, name='api_kas'),
    path('api/column-kas/', api.api_column_kas, name='api_column_kas'),


    path('register-siswa/', auth.register_siswa, name='register-siswa'),
    
]
