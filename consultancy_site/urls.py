from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Connects to your main 'jobs' app
    path('', include('jobs.urls')), 
    
    # Required for django-allauth (Google Login)
    path('accounts/', include('allauth.urls')), 
]