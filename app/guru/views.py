from typing import Any
from django import http
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from app.auth import role_required
from app.atributes import get_hari_ini
from app.models import *
from django.http import HttpResponseNotFound
from django.views.generic.base import View
from django.utils.decorators import method_decorator

url_login = '/login'

# BAGIAN GURU
@login_required(login_url=url_login)
@role_required('guru')
def dashboard_guru(request):
    hari_ini = get_hari_ini()
    piket = JadwalPiket.objects.filter(hari=hari_ini)
    return render(request, 'guru/dashboard.html', {'hari_ini': hari_ini,'piket':piket})



class ListSiswa(View):
    hari = ['none','senin', 'selasa','rabu','kamis','jumat','sabtu']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data = None
        
    def dispatch(self, request, *args, **kwargs):
        self.data = request.user
        self.listsiswa = UserData.objects.filter(role='siswa',id_kelas = self.data.id_kelas)
        return super().dispatch(request, *args, **kwargs)

    @method_decorator(login_required(login_url=url_login))
    @method_decorator(role_required('guru'))
    def get(self,request):
        return render(request,'guru/list-siswa.html',{'siswa':self.listsiswa,'hari':self.hari})
    def post(self,request):
        nama_lengkap = request.POST.get('nama_lengkap')
        no_hp = request.POST.get('no_hp')
        piket = request.POST.get('piket')
        idUser = request.POST.get('idUser')

        if piket is not None or piket != 'none':
            jadwal = JadwalPiket.objects.filter(id_user=idUser,id_kelas=self.data.id_kelas)
            if len(jadwal) <= 0:
                JadwalPiket.create_jadwalPiket(id_user=idUser,id_kelas=self.data.id_kelas.id_kelas,hari=piket)
            else:
                jadwal.update(hari=piket)
        self.listsiswa.filter(id_user=idUser).update(nama_lengkap=nama_lengkap,no_hp=no_hp,)
        return redirect('/list-siswa')

class TugasKelas(View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data = None
        
    def dispatch(self, request, *args, **kwargs):
        self.data = request.user
        self.list_tugas = Tugas.objects.filter(id_pelajaran__id_guru=self.data.id_user)
        self.listPelajaran = Pelajaran.objects.filter(id_guru=self.data.id_user)
        self.listKelas = Kelas.objects.all()
        return super().dispatch(request, *args, **kwargs)
    
    @method_decorator(login_required(login_url=url_login))
    @method_decorator(role_required('guru'))
    def get(self,request):
        context = {
            'list_tugas':self.list_tugas,
            'ddPelajaran':self.listPelajaran,
            'ddKelas':self.listKelas,
        }
        return render(request,'guru/list-tugas.html',context)

    def post(self,request):
        nama_tugas = request.POST.get('nama_tugas')
        pelajaran = request.POST.get('pelajaran')
        tenggat_waktu = request.POST.get('tenggat_waktu')
        deskripsi = request.POST.get('catatan')
        id_tugas = request.POST.get('idTugas','')
        tugas = self.list_tugas.filter(id_tugas=id_tugas)
        if tenggat_waktu is not None:
            tugas.update(end_date=tenggat_waktu)
        tugas.update(nama_tugas=nama_tugas,id_pelajaran=pelajaran,deskripsi=deskripsi)
        return redirect('/tugas-kelas')

@login_required(login_url=url_login)
@role_required('guru')
def profile_user(request, id_user):
    data = request.user
    if id_user == data.id_user:
        return redirect('my-profile')
    try:
        users = UserData.objects.get(id_user=id_user)
        
        return render(request, 'guru/profil-siswa.html', {'data': users,})
    except UserData.DoesNotExist:
        return HttpResponseNotFound()