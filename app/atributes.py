from django.utils import timezone
from django.contrib.auth.models import AnonymousUser
from datetime import datetime

def get_current_month_year():
    current_date = datetime.now()
    month = current_date.strftime('%m')
    year = current_date.strftime('%Y')
    return month,year

current_month_year = get_current_month_year()
month=current_month_year[0]
year = current_month_year[1]

menu_siswa={'siswa':{
    'dashboard': {'url': '/dashboard-siswa/', 'icon': 'bi bi-grid-fill', 'text': 'Dashboard'},
    'jadwal-pelajaran': {'url': '/jadwal-pelajaran/', 'icon': 'bi bi-calendar-event-fill', 'text': 'Jadwal Pelajaran'},
    'jadwal-piket': {'url': '/jadwal-piket/', 'icon': 'bi bi-calendar2-week-fill', 'text': 'Jadwal Piket'},
    'Tugas': {'url': '/tugas', 'icon': 'bi bi-file-earmark-text-fill', 'text': 'Tugas'},
    'kas': {'url': f'/kas/', 'icon': 'bi bi-wallet-fill', 'text': 'Kas Kelas'},
    'boarding': {'url': '/boarding/', 'icon': 'bi bi-easel-fill', 'text': 'Boarding Kelas'},
    'list-pengajar': {'url': '/list-pengajar', 'icon': 'bi bi-person-lines-fill', 'text': 'List Pengajar'},
    'setting': {'url': '/', 'icon': 'settings', 'text': 'Pengaturan','submenu':[{'title':'Umum','link':'/pengaturan-umum'},{'title':'Ubah Password','link':'/ubah-password'}]}, 
    'logout': {'url': '/logout', 'icon': 'bi bi-box-arrow-left', 'text': 'Logout'}},

    'guru':{
        'dashboard': {'url': '/dashboard-guru/', 'icon': 'bi bi-grid-fill', 'text': 'Dashboard'},
    'jadwal-mengajar': {'url': '/jadwal-mengajar', 'icon': 'bi bi-list-task', 'text': 'Jadwal Mengajar'},
    'absensi': {'url': '/absensi', 'icon': 'bi bi-person-check-fill', 'text': 'Absensi'},
    'Tugas Kelas': {'url': '/tugas-kelas', 'icon': 'bi bi-file-earmark-text-fill', 'text': 'Tugas Kelas'},
    'kas': {'url': f'/kas/', 'icon': 'bi bi-wallet-fill', 'text': 'Kas Kelas'},
    'boarding': {'url': '/boarding/', 'icon': 'bi bi-easel-fill', 'text': 'Boarding Kelas'},
    'jadwal-pelajaran': {'url': '/jadwal-pelajaran', 'icon': 'bi bi-calendar-event-fill', 'text': 'Jadwal Pelajaran'},
    'jadwal-piket': {'url': '/jadwal-piket', 'icon': 'bi bi-calendar2-week-fill', 'text': 'Jadwal Piket'},
    'list-wali-murid': {'url': '/', 'icon': 'bi bi-person-lines-fill', 'text': 'Daftar List','submenu':[{'title':'List Siswa','link':'/list-siswa'},
                                                                                                        {'title':'List Wali Murid','link':'/list-wali-murid'},
                                                                                                        {'title':'List Pengajar','link':'/list-pengajar'}]},
    'pengaturan-kelas': {'url': '/edit-jadwal-pelajaran', 'icon': '', 'text': 'Edit Jadwal Pelajaran'},
    'setting': {'url': '/', 'icon': 'settings', 'text': 'Pengaturan','submenu':[{'title':'Umum','link':'/pengaturan-umum'},{'title':'Ubah Password','link':'/ubah-password'}]}, 
    'logout': {'url': '/logout', 'icon': 'bi bi-box-arrow-left', 'text': 'Logout'}
    }
    }


def navbar_data(request):
    active_menu = request.path
    hari_list = ['senin', 'selasa', 'rabu', 'kamis', 'jumat', 'sabtu']
    role = None
    menu = None
    if not isinstance(request.user, AnonymousUser):
        role = request.user.role
        menu = menu_siswa[role]
    return {
        'menus': menu,
        'active_menu': active_menu,
        'hari_list':hari_list,
    }

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