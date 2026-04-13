from django.urls import path
from . import views

urlpatterns = [
    # This creates the URL: yourwebsite.com/management/dashboard/
    path('dashboard/', views.dashboard_view, name='admin_dashboard'),
    path('dashboard/add-job/', views.add_job, name='add_job'),
    path('dashboard/add-category/', views.add_category, name='add_category'),
    
    # FIXED: Added "views." in front of the function names
    path('command-center/applications/', views.all_applications, name='all_applications'),
    path('command-center/applications/<int:app_id>/update/', views.update_application_status, name='update_application_status'),
    path('command-center/jobs/', views.manage_jobs, name='manage_jobs'),
    path('command-center/jobs/<int:job_id>/edit/', views.edit_job, name='edit_job'),
    path('command-center/jobs/<int:job_id>/toggle/', views.toggle_job_status, name='toggle_job_status'),
]