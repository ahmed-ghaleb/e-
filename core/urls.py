from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views  # Add this import
from . import views

app_name = 'core'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.dashboard, name='dashboard'),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),  # Add this line for auth URLs
    path('rds/', include('rds.urls')),
]

# Add this to serve static files during development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Set admin site header and title
admin.site.site_header = "e& Egypt Self-Service Portal Admin"
admin.site.site_title = "e& Egypt Portal Admin"
admin.site.index_title = "Welcome to e& Egypt Self-Service Portal Administration"