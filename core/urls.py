
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static



handler404 = 'app.views.not_found_handler'
handler500 = 'app.views.error_handler_500'
handler403 = 'app.views.error_handler_403'


urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'', include('app.siswa.urls')),
    path(r'', include('app.guru.urls')),
    path(r'', include('app.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
