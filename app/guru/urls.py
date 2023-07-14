from django.urls import path
from app import auth
from app.guru import views
from app.auth import DaftarAkun


urlpatterns = [
    path('dashboard-guru/', views.dashboard_guru, name='home-guru'),
]
    