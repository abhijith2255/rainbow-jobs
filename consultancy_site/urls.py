from django.contrib import admin
from django.urls import path, include
from django.conf import settings             # Add this
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Connects to your main 'jobs' app
    path('', include('jobs.urls')), 
    
    # Required for django-allauth (Google Login)
    path('accounts/', include('allauth.urls')), 
    # Connects to your admin dashboard
    path('management/', include('portal_admin.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)