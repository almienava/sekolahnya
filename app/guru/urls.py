from django.urls import path
from app import auth
from app.guru import views
from app.auth import DaftarAkun
from .views import ListSiswa,TugasKelas

urlpatterns = [
    path('dashboard-guru/', views.dashboard_guru, name='home-guru'),
    path('list-siswa', ListSiswa.as_view(), name='list-siswa'),
    path('siswa/<str:id_user>', views.profile_user, name='profile-siswa'),
    path('tugas-kelas', TugasKelas.as_view() , name='tugas-siswa'),

    

]
    