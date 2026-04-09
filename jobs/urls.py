from django.urls import path
from . import views

urlpatterns = [
    # 1. Home page showing the job list
    path('', views.job_list, name='job_list'), 
    
    # 2. Student Portal for Sign In and Sign Up
    path('portal/', views.student_portal, name='student_portal'), 
    
    # 3. Student Dashboard (Access after login)
    path('dashboard/', views.student_dashboard, name='student_dashboard'), 
    
    # 4. Logout functionality
    path('logout/', views.student_logout, name='logout'), 
]