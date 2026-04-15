from django.urls import path
from . import views

urlpatterns = [
    # Standard Pages
    path('', views.home, name='home'),
    
    # Authentication Pages
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    
    # Login Phone OTP Endpoints (Ajax)
    path('send-otp/', views.send_phone_otp, name='send_otp'),
    path('verify-otp/', views.verify_phone_otp, name='verify_otp'),
    
    # Jobs & Profile
    path('job/<int:job_id>/', views.job_detail, name='job_detail'),
    path('profile/', views.user_profile, name='user_profile'),
    
    # --- Profile Phone Verification Endpoints (Ajax) ---
    path('profile/send-verification-otp/', views.send_profile_otp, name='profile_send_otp'),
    path('profile/confirm-verification-otp/', views.confirm_profile_otp, name='profile_confirm_otp'),
    
    # --- NEW: Profile Email Verification Endpoints (Ajax) ---
    path('profile/send-email-otp/', views.send_email_otp, name='profile_send_email_otp'),
    path('profile/confirm-email-otp/', views.confirm_email_otp, name='profile_confirm_email_otp'),
    # Add this inside your urlpatterns list:
    path('candidate/<str:username>/', views.public_profile, name='public_profile'),
]