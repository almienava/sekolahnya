from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponse
from app.auth import role_required
import datetime
from app.models import *
from datetime import datetime, timedelta
from django.contrib import messages
import requests
from django.contrib.auth.hashers import check_password,make_password
from django.db.models import Sum,Q
from django.utils import timezone
from django.views.generic.base import View,TemplateView


url_login = '/login'

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

def filter_waktu(notif):
    result = []
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
        result.append(x)
    return result


class FiturSiswa(View):
    nama = None
    limit = 25
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data = None

    def dispatch(self, request, *args, **kwargs):
            self.data = request.user
            self.notifModels = Notifikasi_user.objects.filter(id_user=self.data.id_user).order_by('-id_notifikasi__created_at')

            return super().dispatch(request, *args, **kwargs)
    
    @method_decorator(login_required(login_url=url_login))
    @method_decorator(role_required('siswa'))
    def get(self, request):
        path_html = f'siswa/{self.nama}.html'
        
        if self.nama in ['jadwal-piket', 'jadwal-pelajaran',
                          'profil-siswa','list-pengajar']:
            data = {
                'jadwal-piket': JadwalPiket.objects.filter(id_kelas=self.data.id_kelas),
                'jadwal-pelajaran': JadwalPelajaran.objects.filter(id_kelas=self.data.id_kelas),
                'profil-siswa': self.data,
                'list-pengajar':Pelajaran.objects.all()
            }.get(self.nama)
            
            if data is not None:
                return render(request, path_html, {'data': data})
        
        elif self.nama in ['notifikasi-siswa','load-more']:
            path_html = f'siswa/notifikasi/{self.nama}.html'
            notifModelFalse = self.notifModels.filter(status_buka=False)
            TotalNotifFalse = notifModelFalse.count() # menghitung jumlah status yang belum di buka

            offset = int(request.GET.get('offset', 0)) # offset akan bertambah jika scroll,defaultnya 0
            notifModelLoadMore = self.notifModels[offset:offset+self.limit] # ngeload notif dri 0 + limit nya yaitu 10

            # tampilin notif semua tapi dilimit
            result_notif = filter_waktu(self.notifModels[:self.limit])
            # Tapi Kalau Notif yang belum dibuka 
            # lebih dari 10 maka tampilin semua yang belum di buka
            if TotalNotifFalse >= 10:
                result_notif = filter_waktu(self.notifModels[:TotalNotifFalse])
            
            
            notifModelFalse.update(status_buka=True) # untuk update status jika sudah di buka

            data = {'notifikasi-siswa':result_notif,
                    'load-more':filter_waktu(notifModelLoadMore)}.get(self.nama)
            return render(request, path_html, {'notif': data})

        return HttpResponse(status=500)



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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data = None
        self.TugasModel = None
    def dispatch(self, request, *args, **kwargs):
            self.data = request.user
            self.TugasModel = TugasUser.objects.filter(id_user=self.data.id_user)
            return super().dispatch(request, *args, **kwargs)

    @method_decorator(login_required(login_url=url_login))
    @method_decorator(role_required('siswa'))
    def get(self,request):
        TugasData = self.TugasModel.order_by('-id_tugas__created_tugas')
        ddStatus = [
        {'key':0,'value':'Belum Selesai','bg':'light-secondary'},
        {'key':1,'value':'Selesai','bg':'light-success'},
        {'key':2,'value':'Proses','bg':'light-warning'}]
        return render(request,'siswa/tugas-siswa.html',{'data':TugasData,'ddstatus':ddStatus})

    @method_decorator(login_required(login_url=url_login))
    @method_decorator(role_required('siswa'))
    def post(self, request):
        status = request.POST.get('statusTugas')
        note = request.POST.get('catatan')
        idTugas = request.POST.get('idTugas')
        self.TugasModel.filter(id_tugas=idTugas).update(status_tugas=status,catatan_user=note)
        return redirect('tugas-siswa')
    

def kas_data(request):
    data_kas = Kas.objects.filter(id_kelas=request.user.id_kelas)
    total_nominals = data_kas.aggregate(total=Sum('nominal'))['total']   
    total_nominal = "{:,.0f}".format(total_nominals).replace(",", ".")
    return total_nominal


# 1 pemasukan,0 pengeluaran
class KasSiswa(View):
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
    path_html = 'siswa/kas-siswa.html'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data = None
        self.data_kas = None
    def dispatch(self, request, *args, **kwargs):
            self.data = request.user
            self.data_kas = Kas.objects.filter(id_kelas=self.data.id_kelas)
            total_nominals = self.data_kas.aggregate(total=Sum('nominal'))['total']   
            self.total_nominal = "{:,.0f}".format(total_nominals).replace(",", ".")
            self.histori_transaksi = HistoriTransaksiKas.objects.filter(id_kelas = self.data.id_kelas).order_by('-tanggal_histori')
            self.month = request.GET.get('month')
            self.year = request.GET.get('year')
            if self.month is None and self.year is None:
                current_date = datetime.now()
                self.month = current_date.strftime('%m')
                self.year = current_date.strftime('%Y')
            return super().dispatch(request, *args, **kwargs)

    @method_decorator(login_required(login_url=url_login))
    @method_decorator(role_required('siswa'))
    def get(self,request):
        date_string = f"{self.year}-{self.month}-01"
        date = datetime.strptime(date_string, '%Y-%m-%d').date()
        while date.weekday() != 0:  
            date += timedelta(days=1)
        column_dates = []
        while date.strftime('%m') == self.month:
            column_dates.append(date.strftime('%Y-%m-%d'))
            date += timedelta(days=7)  # Lanjut ke hari Senin berikutnya

        
        data_kas_filter = self.data_kas.filter(yearmonth=f'{self.year}{self.month}')
        context={'column_dates':column_dates,'isi':data_kas_filter,
                    'month':self.months,'total_kas':self.total_nominal,
                    'histori':self.histori_transaksi,'nominals':5000}
        return render(request, self.path_html,context)
    @method_decorator(login_required(login_url=url_login))
    @method_decorator(role_required('siswa'))
    def post(self,request):
        pembayaran = request.POST.get('pembayaran')
        # nominal = request.POST.get('NominalKas')
        aksi = request.POST.get('aksi')
        idUser = request.POST.get('idUser')
        kas = self.data_kas.filter(id_user = idUser,yearmonth=f'{self.year}{self.month}')
        value = True
        jenis_ ,deskripsi_= 1,'Bayar Kas'
        if aksi =='reset':
            value=False
            jenis_,deskripsi_ = 0,'Salah Input'

        if pembayaran == 'w1':
            kas.update(w1=value,w1_dtm=datetime.now())
        elif pembayaran == 'w2':
            kas.update(w2=value,w2_dtm=datetime.now())
        elif pembayaran == 'w3':
            kas.update(w3=value,w3_dtm=datetime.now())
        elif pembayaran == 'w4':
            kas.update(w4=value,w4_dtm=datetime.now())
        elif pembayaran == 'w5':
            kas.update(w5=value,w5_dtm=datetime.now())
        userdata = UserData.objects.filter(id_user=idUser)[:1]
        HistoriTransaksiKas.create_histori(id_user=userdata, id_kelas=self.data.id_kelas.id_kelas,
                                                      deskripsi=deskripsi_, jenis=jenis_, nominal=5000)
        return redirect('/kas/')

        





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








@login_required(login_url=url_login)
@role_required('siswa')
def load_more_boarding(request):
    data = request.user
    offset = request.GET.get('offset', 50)
    offset = int(offset)
    limit = int(request.GET.get('limit',50))
    isi = BoardingKelas.objects.filter(id_kelas=data.id_kelas).order_by('-id_boarding')[offset:offset+limit]
    return render(request, 'siswa/load-boarding.html',{'offset':offset,'messages':isi})
    


@login_required(login_url=url_login)
@role_required('siswa')
def boarding_room(request,slug):
    data = request.user
    isi = None
    if int(slug) == data.id_kelas.id_kelas:
        isi = BoardingKelas.objects.filter(id_kelas=data.id_kelas).order_by('-id_boarding')[:50]
    return render(request, "siswa/boarding.html",{'slug':slug,'messages':isi})

# BAGIAN GURU
@login_required(login_url=url_login)
@role_required('guru')
def dashboard_guru(request):
    hari_ini = get_hari_ini()
    piket = JadwalPiket.objects.filter(hari=hari_ini)
    return render(request, 'siswa/dashboard-siswa.html', {'hari_ini': hari_ini,'piket':piket})
