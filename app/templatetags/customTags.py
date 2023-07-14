from django import template
from django.utils import timezone
from datetime import timedelta
import pytz

register = template.Library()

@register.filter(name='split')
def split(str, key):
    return str.split(key)



@register.filter(name='filter_waktu')
def filter_waktu(created_at):
    local_tz = pytz.timezone('Asia/Jakarta')  # Menentukan zona waktu yang diinginkan (UTC+7)
    localized_created_at = timezone.localtime(created_at, local_tz)
    
    now = timezone.now()
    if localized_created_at.date() == now.date():
        waktu_lalu = f'Hari ini {localized_created_at.strftime("%H:%M")} WIB'
    elif localized_created_at.date() == now.date() - timedelta(days=1):
        waktu_lalu = f'Kemarin {localized_created_at.strftime("%H:%M")} WIB'
    else:
        waktu_lalu = localized_created_at.strftime("%d/%m/%Y %H:%M WIB")
    
    return waktu_lalu




