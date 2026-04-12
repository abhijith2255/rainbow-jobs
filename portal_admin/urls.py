# portal_admin/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # This creates the URL: yourwebsite.com/management/dashboard/
    path('dashboard/', views.dashboard_view, name='admin_dashboard'),
    path('dashboard/add-job/', views.add_job, name='add_job'),
    path('dashboard/add-category/', views.add_category, name='add_category'),
]