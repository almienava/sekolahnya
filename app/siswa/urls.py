from django.urls import path
from app import auth
from app.siswa import views
from app.auth import DaftarAkun
from .views import TugasSiswa,FiturSiswa,KasSiswa

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
    path('kas/', KasSiswa.as_view(), name='kas-siswa'),
    path('load-boarding/', views.load_more_boarding, name='load-boarding-siswa'),
    path('boarding/<int:slug>', views.boarding_room, name='boarding-siswa'),


    

    #  =========================================================================
    #  =                              GURU VIEW                               =
    #  =========================================================================


    # =========================================================================

    path('register-siswa/',DaftarAkun.as_view(), name='register-siswa'),
    
]
