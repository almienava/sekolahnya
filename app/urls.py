from django.urls import path
from app import views,auth,api


urlpatterns = [
    #  =========================================================================
    #  =                              SISWA VIEW                               =
    #  =========================================================================
    path('dashboard-siswa/', views.dashboard_siswa, name='home-siswa'),
    path('jadwal-piket/', views.jadwal_piket_siswa, name='jadwal-piket-siswa'),
    path('jadwal-pelajaran/', views.jadwal_pelajaran, name='jadwal-pelajaran-siswa'),
    path('list-pelajaran/', views.list_pelajaran, name='list-pelajaran-siswa'),
    path('my-profile', views.profile_siswa, name='profile-siswa'),
    path('tugas', views.tugas_siswa, name='tugas-siswa'),
    path('ubah-password', views.ganti_password, name='ganti-pas-siswa'),
    path('pengaturan-umum', views.pengaturan_siswa_umum, name='pengaturan-siswa'),
    

    path('kas/', views.kas_siswa, name='kas-siswa'),
    path('login', auth.login_user, name='login-siswa'),
    

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
