from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from app.auth import role_required
from app.atributes import get_hari_ini
from app.models import *


url_login = '/login'

# BAGIAN GURU
@login_required(login_url=url_login)
@role_required('guru')
def dashboard_guru(request):
    hari_ini = get_hari_ini()
    piket = JadwalPiket.objects.filter(hari=hari_ini)
    return render(request, 'guru/dashboard.html', {'hari_ini': hari_ini,'piket':piket})
