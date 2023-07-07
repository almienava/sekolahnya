from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .auth import role_required
import datetime
from .models import *
from django.views.decorators.cache import cache_page
from datetime import datetime, timedelta
from django.contrib import messages
import requests
from django.contrib.auth.hashers import check_password,make_password
from django.db.models import Sum

url_login = '/login'


def error_handler_500(request, exception=None):
    return render(request, '500.html',status=500)

def not_found_handler(request, exception=None):
    return render(request, '404.html', status=404)

def error_handler_403(request, exception=None):
    return render(request, '403.html',status=403)

def get_hari_ini():
    hari_ini = datetime.now().strftime('%A').lower()
    hari_indonesia = {
        'monday': 'senin',
        'tuesday': 'selasa',
        'wednesday': 'rabu',
        'thursday': 'kamis',
        'friday': 'jumat',
        'saturday': 'sabtu',
        'sunday': 'minggu'
    }
    return hari_indonesia.get(hari_ini, '')

@login_required(login_url=url_login)
def kas_data(request):
    data_kas = Kas.objects.filter(id_kelas=request.user.id_kelas)
    total_nominals = data_kas.aggregate(total=Sum('nominal'))['total']   
    total_nominal = "{:,.0f}".format(total_nominals).replace(",", ".")
    return data_kas,total_nominal


# BAGIAN SISWA


#dashboard siswa
@login_required(login_url=url_login)
@role_required('siswa')
def dashboard_siswa(request):
    hari_ini = get_hari_ini()
    user = request.user
    piket = JadwalPiket.objects.filter(hari=hari_ini,id_kelas =user.id_kelas)
    jadwal_pelajaran = JadwalPelajaran.objects.filter(hari=hari_ini,id_kelas =user.id_kelas)
    return render(request, 'siswa/dashboard-siswa.html',
                   {'hari_ini': hari_ini,
                    'piket':piket,'jadwal_pelajaran':jadwal_pelajaran,'total_kas':kas_data(request)[1]})


# jadwal piket siswa
@login_required(login_url=url_login)
@role_required('siswa')
def jadwal_piket_siswa(request):
    jadwal_piket = JadwalPiket.objects.filter(id_kelas=request.user.id_kelas)
    return render(request,'siswa/jadwal-piket.html',{'jadwal_piket':jadwal_piket})

# jadwal pelajaran
@login_required(login_url=url_login)
@role_required('siswa')
def jadwal_pelajaran(request):
    jadwal_pelajaran = JadwalPelajaran.objects.filter(id_kelas=request.user.id_kelas)
    return render(request,'siswa/jadwal-pelajaran.html',{'jadwal_pelajaran':jadwal_pelajaran})

# profil siswa
@login_required(login_url=url_login)
@role_required('siswa')
def profile_siswa(request):
    data = request.user
    return render(request,'siswa/profile-siswa.html',{'data':data})


# tugas siswa
@login_required(login_url=url_login)
@role_required('siswa')
def tugas_siswa(request):
    data = request.user
    result = TugasUser.objects.filter(id_user=data.id_user).order_by('-id_tugas__created_tugas')
    for x in result:
        if x.status_tugas == 0:
            x.status_tugas,x.bg = 'Belum Selesai','secondary'
        elif x.status_tugas == 1:
            x.status_tugas,x.bg = 'Selesai','success'
        elif x.status_tugas == 2:
            x.status_tugas,x.bg = 'Proses','warning'
        else:
            x.status_tugas,x.bg = 'Error','error'

    ddStatus = [
        {'key':0,'value':'Belum Selesai'},
        {'key':1,'value':'Selesai'},
        {'key':2,'value':'Proses'}]
    
    if request.method == 'POST':
        status = request.POST.get('statusTugas')
        note = request.POST.get('catatan')
        idTugas = request.POST.get('idTugas')

        TugasUser.objects.filter(id_user=data.id_user,id_tugas=idTugas).update(status_tugas=status,catatan_user=note)
        return redirect('/tugas')
    return render(request,'siswa/tugas-siswa.html',{'data':result,'ddstatus':ddStatus})


# ganti password / ubah password
@login_required(login_url=url_login)
@role_required('siswa')
def ganti_password(request):
    data = request.user
    if request.method == 'POST':
        password_lama = request.POST.get('password_lama')
        password_baru = request.POST.get('password_baru')
        password_confirm = request.POST.get('password_confirm')
        pw = check_password(password_lama, data.password) 
        if password_baru != password_confirm:
            messages.warning(request,'Password Baru tidak sama')
        elif len(password_baru) < 8:
            messages.warning(request,'Password harus lebih dari 8 karakter')
        elif not pw:
            messages.error(request, 'Password Lama Salah!')
        elif password_baru == password_confirm and len(password_baru) >= 8 and pw:
            new_pass = make_password(password_baru)
            UserData.objects.filter(id_user=data.id_user).update(password=new_pass)
            messages.success(request,'Password berhasil diubah!')

    return render(request,'siswa/ganti-pass.html',{'data':data})


# edit akun siswa / pengaturan umum siswa
@login_required(login_url=url_login)
@role_required('siswa')
def pengaturan_siswa_umum(request):
    data = request.user
    if request.method == 'POST':
        nama_lengkap = request.POST.get('nama_lengkap')
        username = request.POST.get('username')
        email = request.POST.get('email')
        foto = request.FILES.get('avatar')        
        if foto:
            url = 'https://api.imgbb.com/1/upload'
            api_key = '50e8f835ca01379d69ca7dd7767eb386'
            payload = {
                'key': api_key,
            }
            file = {
                'image':foto
            }
            response = requests.post(url, params=payload,files=file)
            datas = response.json()

            if datas['success']:
                image = datas['data']['image']['url']
                UserData.objects.filter(id_user=data.id_user).update(
                    profile_pic=image,
                    username = username,
                    email = email,
                    nama_lengkap = nama_lengkap) 
                return redirect('/pengaturan-umum')
            else:
                
                return render(request, 'siswa/pengaturan_umum.html', {'error_message': 'Terjadi kesalahan saat memperbarui data.'})
        else:
            UserData.objects.filter(id_user=data.id_user).update(
                username = username,
                email = email,
                nama_lengkap = nama_lengkap)
            return redirect('/pengaturan-umum')
    return render(request,'siswa/pengaturan-umum.html',{'data':data})

# list pelajaran / list guru
@login_required(login_url=url_login)
@role_required('siswa')
def list_pelajaran(request):
    list_pelajaran = Pelajaran.objects.all()
    return render(request,'siswa/list-pelajaran.html',{'list_pelajaran':list_pelajaran})

# kas siswa
@login_required(login_url=url_login)
@role_required('siswa')
def kas_siswa(request):
    months = {
                "01": "Januari",
                "02": "Februari",
                "03": "Maret",
                "04": "April",
                "05": "Mei",
                "06": "Juni",
                "07": "Juli",
                "08": "Augustus",
                "09": "September",
                "10": "Oktober",
                "11": "November",
                "12": "Desember"}

    month = request.GET.get('month')
    year = request.GET.get('year')

    if month is None and year is None:
        current_date = datetime.now()
        month = current_date.strftime('%m')
        year = current_date.strftime('%Y')
        
    date_string = f"{year}-{month}-01"
    date = datetime.strptime(date_string, '%Y-%m-%d').date()


    while date.weekday() != 0:  
        date += timedelta(days=1)
    column_dates = []
    while date.strftime('%m') == month:
        column_dates.append(date.strftime('%Y-%m-%d'))
        date += timedelta(days=7)  # Lanjut ke hari Senin berikutnya

    header = months.get(month,'')
    header = f"{header} {year}"
    data_kas = kas_data(request)

    return render(request, 'siswa/kas-siswa.html',{'column_dates':column_dates,
                                                    'isi':data_kas[0],
                                                    'month':months,
                                                    'total_kas':data_kas[1],
                                                    'header':header})



# BAGIAN GURU
@login_required(login_url=url_login)
@role_required('guru')
def dashboard_guru(request):
    hari_ini = get_hari_ini()
    piket = JadwalPiket.objects.filter(hari=hari_ini)
    return render(request, 'siswa/dashboard-siswa.html', {'hari_ini': hari_ini,'piket':piket})
