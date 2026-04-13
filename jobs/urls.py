from django.urls import path
from . import views

urlpatterns = [
    # Standard Pages
    path('', views.home, name='home'),
    
    # Authentication Pages
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    
    # Phone OTP Endpoints (Ajax)
    path('send-otp/', views.send_phone_otp, name='send_otp'),
    path('verify-otp/', views.verify_phone_otp, name='verify_otp'),
    path('job/<int:job_id>/', views.job_detail, name='job_detail'),
    
]