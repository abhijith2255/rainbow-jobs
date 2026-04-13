import random
import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from .models import PhoneOTP
from .models import Job, Category, JobApplication  # Make sure to import JobApplication if you have it defined in models.py

# ==========================================
# 1. MAIN PAGES
# ==========================================

# Make sure you import your models at the top of views.py!
from .models import Job, Category 

# ==========================================
# 1. MAIN PAGES
# ==========================================

def home(request):
    """Renders the main Rainbow Jobs landing page with active jobs."""
    # Fetch all categories and only jobs that are marked as active
    categories = Category.objects.all()
    active_jobs = Job.objects.filter(is_active=True).order_by('-created_at') # Newest first
    
    context = {
        'categories': categories,
        'jobs': active_jobs,
    }
    return render(request, 'index.html', context)

# Add this quick placeholder view so our "View Details" button doesn't crash
def job_detail(request, job_id):
    """Renders the full details of a specific job and handles applications."""
    job = get_object_or_404(Job, id=job_id)
    
    # --- NEW: Handle the Application Form Submission ---
    if request.method == 'POST':
        name = request.POST.get('applicant_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        resume = request.POST.get('resume_link')
        cover = request.POST.get('cover_letter')
        
        # Save it to the database
        JobApplication.objects.create(
            job=job,
            applicant_name=name,
            email=email,
            phone=phone,
            resume_link=resume,
            cover_letter=cover
        )
        
        # Send a success alert to the user
        messages.success(request, f"Success! Your application for '{job.title}' has been submitted securely.")
        return redirect('job_detail', job_id=job.id)
    # ---------------------------------------------------

    similar_jobs = Job.objects.filter(
        category=job.category, 
        is_active=True
    ).exclude(id=job.id).order_by('-created_at')[:3]
    
    context = {
        'job': job,
        'similar_jobs': similar_jobs,
    }
    return render(request, 'job_detail.html', context)

def login_view(request):
    """Handles standard username and password login."""
    # If they are already logged in, send them to their proper home
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('admin_dashboard')
        return redirect('home')

    if request.method == 'POST':
        user_name = request.POST.get('username')
        pass_word = request.POST.get('password')

        # Check if the user exists and password matches
        user = authenticate(request, username=user_name, password=pass_word)

        if user is not None:
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            
            # --- SMART REDIRECT ---
            if user.is_superuser:
                return redirect('admin_dashboard') # Admins go to Command Center
            else:
                return redirect('home')            # Users go to job collection
            # ----------------------
            
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('login')

    # If it's a normal visit (GET request), show the login page
    return render(request, 'login.html') 

def register_view(request):
    """Handles new user registration."""
    if request.method == 'POST':
        user_name = request.POST.get('username')
        email = request.POST.get('email')
        pass_word = request.POST.get('password')

        # Check if username already exists
        if User.objects.filter(username=user_name).exists():
            messages.error(request, 'Username already taken.')
            return redirect('login')

        # Check if email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
            return redirect('login')

        # Create the new user
        user = User.objects.create_user(username=user_name, email=email, password=pass_word)
        user.save()
        
        # Automatically log them in after registering
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return redirect('home')

    return render(request, 'login.html')

def logout_view(request):
    """Logs the user out and sends them home."""
    logout(request)
    return redirect('home')

# ==========================================
# 3. PHONE OTP AUTHENTICATION (AJAX)
# ==========================================

def send_phone_otp(request):
    """Generates a 6-digit code and sends it via Fast2SMS."""
    if request.method == 'POST':
        phone = request.POST.get('phone_number')
        
        if not phone:
            return JsonResponse({'status': 'error', 'message': 'Phone number required.'})
        
        # Generate a random 6-digit code
        otp_code = str(random.randint(100000, 999999))
        
        # Save or update it in the database
        PhoneOTP.objects.update_or_create(
            phone_number=phone,
            defaults={'otp': otp_code}
        )
        
        # --- FAST2SMS API INTEGRATION ---
        url = "https://www.fast2sms.com/dev/bulkV2"
        api_key = "OfyY71G2cPhzTlR3vInoNjsM5pmwgkWqFSu0dZDrJQL4V9Kba6ogP8skYQAEmcLUHIMfTbRy046VK7rO"  # Keep this safe!
        
        querystring = {
            "authorization": api_key,
            "message": f"Your Rainbow Jobs login code is {otp_code}",
            "language": "english",
            "route": "q",
            "numbers": phone
        }
        headers = {'cache-control': "no-cache"}
        
        try:
            # Send the request to Fast2SMS
            response = requests.request("GET", url, headers=headers, params=querystring)
            response_data = response.json()
            
            if response_data.get('return') == True:
                return JsonResponse({'status': 'success', 'message': 'OTP Sent to your phone!'})
            else:
                # 1. Print the REAL error secretly in your terminal for YOU
                print("Fast2SMS Blocked:", response_data) 
                
                # 2. Show a professional, polite message to the USER
                return JsonResponse({'status': 'error', 'message': 'Phone verification is temporarily unavailable. Please use Google Login.'})
                
        except Exception as e:
            print(f"Server SMS Error: {e}")
            return JsonResponse({'status': 'error', 'message': 'System is currently busy. Please try again later.'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})


def verify_phone_otp(request):
    """Verifies the code and logs the user in."""
    if request.method == 'POST':
        phone = request.POST.get('phone_number')
        user_otp = request.POST.get('otp')
        
        try:
            # Find the OTP record for this phone number
            db_record = PhoneOTP.objects.get(phone_number=phone)
            
            if db_record.otp == user_otp:
                # Success! Get the user (or create a new account using their phone number)
                user, created = User.objects.get_or_create(username=phone)
                
                # Log them in securely
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                
                # Delete the OTP from the database so it cannot be reused
                db_record.delete()
                
                # --- SMART REDIRECT FOR AJAX ---
                if user.is_superuser:
                    return JsonResponse({'status': 'success', 'redirect': '/management/dashboard/'})
                else:
                    return JsonResponse({'status': 'success', 'redirect': '/'})
                # -------------------------------
                
            else:
                return JsonResponse({'status': 'error', 'message': 'Invalid OTP code. Please try again.'})
                
        except PhoneOTP.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Session expired. Please request a new OTP.'})
            
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})