from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import JobPosting

# 1. Main Job List View (Updated)
def job_list(request):
    # Fetch jobs, newest first
    jobs = JobPosting.objects.all().order_by('-posted_at')
    return render(request, 'job_list.html', {'jobs': jobs})

# 2. Unified Student Authentication View
def student_portal(request):
    if request.method == 'POST':
        auth_type = request.POST.get('auth_type')

        # --- Sign Up Functionality ---
        if auth_type == 'signup':
            full_name = request.POST.get('full_name')
            email = request.POST.get('email')
            password = request.POST.get('password')

            if User.objects.filter(username=email).exists():
                messages.error(request, "This email is already registered.")
            else:
                # Use email as the username for simplicity
                user = User.objects.create_user(username=email, email=email, password=password)
                user.first_name = full_name
                user.save()
                login(request, user)
                messages.success(request, f"Welcome to Rainbow Jobs, {full_name}!")
                return redirect('student_dashboard')

        # --- Sign In Functionality ---
        elif auth_type == 'signin':
            email = request.POST.get('email')
            password = request.POST.get('password')
            user = authenticate(request, username=email, password=password)
            
            if user is not None:
                login(request, user)
                return redirect('student_dashboard')
            else:
                messages.error(request, "Invalid credentials. Please try again.")

    return render(request, 'login.html')

# 3. Logout Functionality
def student_logout(request):
    logout(request)
    return redirect('job_list')

# 4. Student Dashboard (Placeholder for your presentation)
def student_dashboard(request):
    if not request.user.is_authenticated:
        return redirect('student_portal')
    return render(request, 'dashboard.html')