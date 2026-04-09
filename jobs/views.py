from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import JobPosting

# 1. Main Job List View (Updated)
def home(request):
    # Fetch jobs, newest first
    
    return render(request, 'index.html')

