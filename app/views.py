from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .auth import role_required
import datetime
from .models import *
from datetime import datetime, timedelta
from django.contrib import messages
import requests
from django.contrib.auth.hashers import check_password,make_password
from django.db.models import Sum,Q
from django.utils import timezone
from django.views import View

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
    tugas = TugasUser.objects.filter(Q(id_user=user.id_user))

    
    tugas_selesai = tugas.filter(Q(status_tugas=1)).count()
    tugas_ = tugas.filter(Q(status_tugas=0))|tugas.filter(status_tugas=2)
    tugas_tersedia = tugas_.count()

    notif = Notifikasi_user.objects.filter(status_buka = False,id_user=user.id_user).count()
    return render(request, 'siswa/dashboard-siswa.html',
                   {'hari_ini': hari_ini,
                    'piket':piket,'jadwal_pelajaran':jadwal_pelajaran,
                    'total_kas':kas_data(request)[1],'tugas_selesai':tugas_selesai,
                    'tugas_tersedia':tugas_tersedia,'count_notif':notif})


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

@login_required(login_url=url_login)
@role_required('siswa')
def profile_user(request,username_user):
    data = request.user
    if username_user == data.username:
        return redirect('profile-siswa')
    users = UserData.objects.filter(username=username_user)
    if len(users) == 0:
        return redirect('home-siswa')
    return render(request,'siswa/profile-user.html',{'data':users})



class TugasSiswa(View):
    def get(self,request):
        self.data = request.user
        self.TugasModel = TugasUser.objects.filter(id_user=self.data.id_user)
        TugasData = self.TugasModel.order_by('-id_tugas__created_tugas')
        ddStatus = [
        {'key':0,'value':'Belum Selesai','bg':'light-secondary'},
        {'key':1,'value':'Selesai','bg':'light-success'},
        {'key':2,'value':'Proses','bg':'light-warning'}]

        return render(request,'siswa/tugas-siswa.html',{'data':TugasData,'ddstatus':ddStatus})

    def post(self, request):
        status = request.POST.get('statusTugas')
        note = request.POST.get('catatan')
        idTugas = request.POST.get('idTugas')

        self.TugasModel.objects.filter(id_tugas=idTugas).update(status_tugas=status,catatan_user=note)
        return redirect('tugas-siswa')
    
@login_required(login_url=url_login)
@role_required('siswa')
def tugas_siswa(request):
    data = request.user
    result = TugasUser.objects.filter(id_user=data.id_user).order_by('-id_tugas__created_tugas')
    ddStatus = [
        {'key':0,'value':'Belum Selesai','bg':'light-secondary'},
        {'key':1,'value':'Selesai','bg':'light-success'},
        {'key':2,'value':'Proses','bg':'light-warning'}]
    
    if request.method == 'POST':
        status = request.POST.get('statusTugas')
        note = request.POST.get('catatan')
        idTugas = request.POST.get('idTugas')

        TugasUser.objects.filter(id_user=data.id_user,id_tugas=idTugas).update(status_tugas=status,catatan_user=note)
        return redirect('/tugas')
    return render(request,'siswa/tugas-siswa.html',{'data':result,'ddstatus':ddStatus})




def data_notif(request):
    notif = Notifikasi_user.objects.filter(id_user=request.user.id_user).order_by('-id_notifikasi__created_at')
    isi = []
    for x in notif:
        created_at = x.id_notifikasi.created_at
        now = timezone.now()
        selisih = now - created_at
        if selisih < timedelta(minutes=1):
            waktu_lalu = 'Baru saja'
        elif selisih < timedelta(hours=1):
            waktu_lalu = f'{selisih.seconds // 60} menit lalu'
        elif selisih < timedelta(days=1):
            waktu_lalu = f'{selisih.seconds // 3600} jam lalu'
        elif selisih < timedelta(days=7):
            waktu_lalu = f'{selisih.days} hari lalu'
        elif selisih < timedelta(days=31):
            waktu_lalu = f'{selisih.days // 7} minggu lalu'
        else:
            waktu_lalu = f'{selisih.days // 31} bulan lalu'
        x.id_notifikasi.created_at = waktu_lalu
        isi.append(x)
    return isi,notif

@login_required(login_url=url_login)
@role_required('siswa')
def loadmore_notif_siswa(request):
    offset = int(request.GET.get('offset', 0))
    limit = 5
    notif = data_notif(request)[0][offset:offset+limit]
    return render(request, 'siswa/notifikasi/load-more.html',{'notif':notif})

@login_required(login_url=url_login)
@role_required('siswa')
def notifikasi_siswa(request):
    notif = data_notif(request)[1]
    notif_filter = notif.filter(status_buka=False).count()
    count = 10
    isi = data_notif(request)[0]
    if notif_filter > 10 :
        count = notif_filter
    notif_ = isi[:count]
    
    notif.update(status_buka=True)
    return render(request,'siswa/notifikasi/notifikasi-siswa.html',{'notif':notif_})


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
                image = datas['data']['thumb']['url']
                UserData.objects.filter(id_user=data.id_user).update(
                    profile_pic=image,
                    username = username,
                    email = email,
                    nama_lengkap = nama_lengkap) 
                return redirect('pengaturan-siswa')
            else:
                
                return render(request, 'siswa/pengaturan_umum.html', {'error_message': 'Terjadi kesalahan saat memperbarui data.'})
        else:
            UserData.objects.filter(id_user=data.id_user).update(
                username = username,
                email = email,
                nama_lengkap = nama_lengkap)
            return redirect('pengaturan-siswa')
    return render(request,'siswa/pengaturan-umum.html',{'data':data})

# list pelajaran / list guru
@login_required(login_url=url_login)
@role_required('siswa')
def list_pengajar(request):
    list_pengajar = Pelajaran.objects.all()
    return render(request,'siswa/list-pengajar.html',{'list_pengajar':list_pengajar})

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


@login_required(login_url=url_login)
@role_required('siswa')
def boarding_siswa(request):
    data = request.user
    return render(request, 'siswa/boarding.html')



# BAGIAN GURU
@login_required(login_url=url_login)
@role_required('guru')
def dashboard_guru(request):
    hari_ini = get_hari_ini()
    piket = JadwalPiket.objects.filter(hari=hari_ini)
    return render(request, 'siswa/dashboard-siswa.html', {'hari_ini': hari_ini,'piket':piket})
