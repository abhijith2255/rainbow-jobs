from django.urls import path
from . import views

urlpatterns = [
    # 1. Home page showing the job list
    path('', views.home, name='home'), 
    
]