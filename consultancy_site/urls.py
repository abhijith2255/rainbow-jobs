from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # The empty string '' here makes the jobs app the main homepage
    path('', include('jobs.urls')), 
]