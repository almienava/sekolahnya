from django.urls import path
from app import views,auth,api
from app.auth import LoginUser,DaftarAkun
from app.views import TugasSiswa,FiturSiswa

urlpatterns = [
    #  =========================================================================
    #  =                              SISWA VIEW                               =
    #  =========================================================================
    path('dashboard-siswa/', views.dashboard_siswa, name='home-siswa'),
    path('jadwal-piket/', FiturSiswa.as_view(nama='jadwal-piket'), name='jadwal-piket-siswa'),
    path('jadwal-pelajaran/', FiturSiswa.as_view(nama='jadwal-pelajaran'), name='jadwal-pelajaran-siswa'),
    path('list-pengajar', FiturSiswa.as_view(nama='list-pengajar'), name='list-pengajar-siswa'),
    path('my-profile',FiturSiswa.as_view(nama='profil-siswa'), name='profile-siswa'),
    path('profile/<str:username_user>', views.profile_user, name='profile-user'),
    path('tugas', TugasSiswa.as_view(), name='tugas-siswa'),
    path('ubah-password', views.ganti_password, name='ganti-pas-siswa'),
    path('pengaturan-umum', views.pengaturan_siswa_umum, name='pengaturan-siswa'),
    path('notifikasi/', FiturSiswa.as_view(nama='notifikasi-siswa'), name='notifikasi-siswa'),
    path('load-more-siswa/', FiturSiswa.as_view(nama='load-more'), name='load_more_notif_siswa'),
    path('kas/', views.kas_siswa, name='kas-siswa'),

    path('login', LoginUser.as_view(), name='login'),
    path('boarding/', views.boarding_siswa, name='boarding-siswa'),

    

    #  =========================================================================
    #  =                              GURU VIEW                               =
    #  =========================================================================
    path('dashboard-guru/', views.dashboard_guru, name='home-guru'),
    

    # =========================================================================

    path('logout/', auth.logout_view, name='logout'),

    path('api/kas/', api.api_kas, name='api_kas'),
    path('api/column-kas/', api.api_column_kas, name='api_column_kas'),


    path('register-siswa/',DaftarAkun.as_view(), name='register-siswa'),
    
]
