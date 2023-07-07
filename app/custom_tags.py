







"""
CUSTOM TAGS NANTI LANGSUNG COPY SCRIPT INI KEDALAM FILE
YANG ADA PADA LIBRARY DJANGO/TEMPLATE/DEFAULTFILTERS.PY 

"""

from django import template

register = template.Library()

@register.filter(name='split')
def split(str, key):
    return str.split(key)