from django.contrib.auth.decorators import login_required
from .auth import role_required
from django.http import JsonResponse
from .models import Kas,UserData
from datetime import datetime, timedelta

url_login_siswa = '/login-siswa/'

@login_required(login_url=url_login_siswa)
@role_required('siswa')
def api_kas(request):
    try:
        month = request.GET.get('month')
        year = request.GET.get('year')
        date_string = f"{year}-{month}-01"
        date = datetime.strptime(date_string, '%Y-%m-%d').date()
        while date.weekday() != 0:  # 0 adalah kode hari Senin
            date += timedelta(days=1)
        
        column_dates = []
        while date.strftime('%m') == month:
            column_dates.append(date.strftime('%Y-%m-%d'))
            date += timedelta(days=7)  # Lanjut ke hari Senin berikutnya


        id_kelas = request.user.id_user
        if len(column_dates) == 4:
            data_kas = Kas.objects.filter().values()
        elif len(column_dates) == 3:
            data_kas = Kas.objects.filter().values()
        respons_data = list(data_kas)
        for data in respons_data:
            id_users = data['id_user_id']
            user = UserData.objects.get(id_user=id_users)
            data['nama_user'] = user.nama_lengkap

        column_dates.insert(0, 'Nama Siswa')
        column_dates.append('Edit')

        return JsonResponse({'isi':respons_data,'column':column_dates},safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)})
    


def api_column_kas(request):
    try:
        # Ambil parameter bulan dan tahun dari request.GET
        month = request.GET.get('month')
        year = request.GET.get('year')

        date_string = f"{year}-{month}-01"
        date = datetime.strptime(date_string, '%Y-%m-%d').date()

        # Cari tanggal hari Senin pertama di bulan tersebut
        while date.weekday() != 0:  # 0 adalah kode hari Senin
            date += timedelta(days=1)

        # Buat daftar tanggal hari Senin dalam bulan tersebut
        column_dates = []
        while date.strftime('%m') == month:
            column_dates.append(date.strftime('%Y-%m-%d'))
            date += timedelta(days=7)  # Lanjut ke hari Senin berikutnya

        return JsonResponse({'column_dates': column_dates})
    except Exception as e:
        return JsonResponse({'error': str(e)})
