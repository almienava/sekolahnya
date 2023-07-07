from django.utils import timezone

from datetime import datetime

def get_current_month_year():
    current_date = datetime.now()
    month = current_date.strftime('%m')
    year = current_date.strftime('%Y')
    return month,year

current_month_year = get_current_month_year()
month=current_month_year[0]
year = current_month_year[1]

menu_siswa={
    'dashboard': {'url': '/dashboard-siswa/', 'icon': 'bi bi-grid-fill', 'text': 'Dashboard'},
    'jadwal-pelajaran': {'url': '/jadwal-pelajaran/', 'icon': 'bi bi-calendar-event-fill', 'text': 'Jadwal Pelajaran'},
    'jadwal-piket': {'url': '/jadwal-piket/', 'icon': 'bi bi-calendar2-week-fill', 'text': 'Jadwal Piket'},
    'Tugas': {'url': '/tugas', 'icon': 'bi bi-file-earmark-text-fill', 'text': 'Tugas'},
    'kas': {'url': f'/kas/', 'icon': 'bi bi-wallet-fill', 'text': 'Kas Kelas'},
    'boarding': {'url': '/boarding/', 'icon': 'bi bi-easel-fill', 'text': 'Boarding Kelas'},
    'list-pelajaran': {'url': '/list-pelajaran/', 'icon': 'bi bi-person-lines-fill', 'text': 'List Pelajaran'},
    'setting': {'url': '/', 'icon': 'bi bi-gear-fill', 'text': 'Pengaturan','submenu':[{'title':'Umum','link':'/pengaturan-umum'},{'title':'Ubah Password','link':'/ubah-password'}]}, 
    'logout': {'url': '/logout', 'icon': 'bi bi-box-arrow-left', 'text': 'Logout'}, 
    }


def navbar_data(request):
    active_menu = request.path
    hari_list = ['senin', 'selasa', 'rabu', 'kamis', 'jumat', 'sabtu']
    
    return {
        'menus': menu_siswa,
        'active_menu': active_menu,
        'hari_list':hari_list,
    }