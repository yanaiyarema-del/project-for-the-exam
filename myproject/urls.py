from django.contrib import admin
from django.urls import path, include
from .views import home_view    
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', home_view, name='home'),
    path('users/', include('users.urls')),
    path('admin/', admin.site.urls),
    path('books/', include('books.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
