import random
import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Count, Q

# Import all your models
from .models import Job, Category, JobApplication, PhoneOTP

# Helper function to check if user is an admin/employer
def is_admin(user):
    return user.is_superuser

# ==========================================
# 1. PUBLIC PAGES
# ==========================================



from django.db.models import Count, Q

def home(request):
    """Renders the main Rainbow Jobs landing page with active jobs."""
    
    # 1. Fetch only ACTIVE jobs
    active_jobs = Job.objects.filter(is_active=True).order_by('-created_at')
    
    # 2. THE FIX: Changed 'job' to 'jobs' in the Count and Q filter
    categories = Category.objects.annotate(
        active_job_count=Count('jobs', filter=Q(jobs__is_active=True))
    ).filter(active_job_count__gt=0)
    
    context = {
        'categories': categories,
        'jobs': active_jobs,
    }
    return render(request, 'index.html', context)


def job_detail(request, job_id):
    """Renders the full details of a specific job and handles applications."""
    job = get_object_or_404(Job, id=job_id)
    
    # Handle the Application Form Submission
    if request.method == 'POST':
        name = request.POST.get('applicant_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        resume = request.POST.get('resume_link')
        cover = request.POST.get('cover_letter')
        
        # Save to database
        JobApplication.objects.create(
            job=job, applicant_name=name, email=email, 
            phone=phone, resume_link=resume, cover_letter=cover
        )
        
        messages.success(request, f"Success! Your application for '{job.title}' has been submitted securely.")
        return redirect('job_detail', job_id=job.id)

    # Find similar jobs
    similar_jobs = Job.objects.filter(category=job.category, is_active=True).exclude(id=job.id).order_by('-created_at')[:3]
    
    return render(request, 'job_detail.html', {'job': job, 'similar_jobs': similar_jobs})


# ==========================================
# 2. AUTHENTICATION (Login, Register, Logout)
# ==========================================

def login_view(request):
    """Handles standard username and password login."""
    if request.user.is_authenticated:
        return redirect('admin_dashboard') if request.user.is_superuser else redirect('home')

    if request.method == 'POST':
        user_name = request.POST.get('username')
        pass_word = request.POST.get('password')

        user = authenticate(request, username=user_name, password=pass_word)

        if user is not None:
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('admin_dashboard') if user.is_superuser else redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('login')

    return render(request, 'login.html') 


def register_view(request):
    """Handles new user registration."""
    if request.method == 'POST':
        user_name = request.POST.get('username')
        email = request.POST.get('email')
        pass_word = request.POST.get('password')

        if User.objects.filter(username=user_name).exists():
            messages.error(request, 'Username already taken.')
            return redirect('login')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
            return redirect('login')

        user = User.objects.create_user(username=user_name, email=email, password=pass_word)
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return redirect('home')

    return render(request, 'login.html')


def logout_view(request):
    """Logs the user out and sends them home."""
    logout(request)
    return redirect('home')


# ==========================================
# 3. PREMIUM CANDIDATE PROFILE
# ==========================================

@login_required(login_url='login')
def user_profile(request):
    if request.method == 'POST':
        user = request.user
        profile = user.profile
        
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.save()
        
        profile.headline = request.POST.get('headline', profile.headline)
        profile.bio = request.POST.get('bio', profile.bio)
        profile.location = request.POST.get('location', profile.location)
        profile.dob = request.POST.get('dob') if request.POST.get('dob') else profile.dob
        profile.gender = request.POST.get('gender', profile.gender)
        
        if 'profile_picture' in request.FILES:
            profile.profile_picture = request.FILES['profile_picture']
        if 'resume' in request.FILES:
            profile.resume = request.FILES['resume']
            
        profile.save()
        messages.success(request, "Profile updated successfully!")
        return redirect('user_profile')
    return render(request, 'profile.html')


# ==========================================
# 4. FAST2SMS PHONE VERIFICATION (AJAX)
# ==========================================

# NOTE: In production, store this API Key in a .env file!
FAST2SMS_API_KEY = "OfyY71G2cPhzTlR3vInoNjsM5pmwgkWqFSu0dZDrJQL4V9Kba6ogP8skYQAEmcLUHIMfTbRy046VK7rO"

@login_required
def send_profile_otp(request):
    """Sends OTP for profile verification with a Localhost Bypass."""
    if request.method == 'POST':
        phone = request.POST.get('phone_number')
        if not phone:
            return JsonResponse({'status': 'error', 'message': 'Please enter a valid phone number.'})
        
        # 1. Save phone to profile
        request.user.profile.phone_number = phone
        request.user.profile.save()

        # 2. Generate OTP & Save to Database
        otp_code = str(random.randint(100000, 999999))
        PhoneOTP.objects.update_or_create(phone_number=phone, defaults={'otp': otp_code})
        
        # 3. Print the code to your terminal so you can test on localhost!
        print("\n" + "="*30)
        print(f"  DEV MODE OTP: {otp_code}")
        print(f"  FOR PHONE: {phone}")
        print("="*30 + "\n")

        # 4. Attempt to send real SMS (will likely fail on localhost)
        url = "https://www.fast2sms.com/dev/bulkV2"
        querystring = {
            "authorization": FAST2SMS_API_KEY,
            "variables_values": otp_code,
            "route": "otp",
            "numbers": phone
        }
        
        try:
            response = requests.request("GET", url, headers={'cache-control': "no-cache"}, params=querystring)
            response_data = response.json()
            
            if response_data.get('return') == True:
                return JsonResponse({'status': 'success', 'message': 'OTP sent to your phone!'})
            else:
                # --- THE BYPASS ---
                # Even if Fast2SMS fails (because of website verification), we return 'success'
                # so your Modal opens and you can type the code from the terminal.
                return JsonResponse({
                    'status': 'success', 
                    'message': f'Dev Mode: Code {otp_code} printed to terminal (Fast2SMS blocked on localhost).'
                })
        except Exception:
            # Fallback success for system errors
            return JsonResponse({'status': 'success', 'message': 'Dev Mode: Check terminal for code.'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request.'})


@login_required
def confirm_profile_otp(request):
    """Checks the OTP and marks the logged-in user's phone as verified."""
    if request.method == 'POST':
        user_otp = request.POST.get('otp')
        phone = request.user.profile.phone_number 
        
        try:
            db_record = PhoneOTP.objects.get(phone_number=phone)
            if db_record.otp == user_otp:
                request.user.profile.is_phone_verified = True
                request.user.profile.save()
                db_record.delete() # Clean up OTP
                return JsonResponse({'status': 'success', 'message': 'Verified successfully!'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Incorrect OTP code.'})
        except PhoneOTP.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Session expired.'})


# ==========================================
# 5. ADMIN COMMAND CENTER
# ==========================================

@login_required(login_url='login')
@user_passes_test(is_admin, login_url='home')
def admin_dashboard(request):
    """Main dashboard for site administrators."""
    return render(request, 'admin_dashboard.html')


@login_required(login_url='login')
@user_passes_test(is_admin, login_url='home')
def manage_jobs(request):
    """Admin view to manage, edit, and hide job postings."""
    jobs = Job.objects.all().order_by('-created_at')
    categories = Category.objects.all()
    return render(request, 'admin_manage_jobs.html', {'jobs': jobs, 'categories': categories})


@login_required(login_url='login')
@user_passes_test(is_admin, login_url='home')
def toggle_job_status(request, job_id):
    """Instantly hides or shows a job on the public site."""
    job = get_object_or_404(Job, id=job_id)
    job.is_active = not job.is_active
    job.save()
    
    status_text = "Activated" if job.is_active else "Hidden"
    messages.success(request, f"Job '{job.title}' is now {status_text}.")
    return redirect('manage_jobs')


@login_required(login_url='login')
@user_passes_test(is_admin, login_url='home')
def all_applications(request):
    """The ATS (Applicant Tracking System) view."""
    applications = JobApplication.objects.all().order_by('-applied_at')
    return render(request, 'admin_ats.html', {'applications': applications})

# ==========================================
# ORIGINAL LOGIN OTP FUNCTIONS
# ==========================================

def send_phone_otp(request):
    """Generates a 6-digit code and sends it via Fast2SMS for LOGIN/REGISTRATION."""
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
        api_key = "OfyY71G2cPhzTlR3vInoNjsM5pmwgkWqFSu0dZDrJQL4V9Kba6ogP8skYQAEmcLUHIMfTbRy046VK7rO"
        
        querystring = {
            "authorization": api_key,
            "message": f"Your Rainbow Jobs login code is {otp_code}",
            "language": "english",
            "route": "q",
            "numbers": phone
        }
        
        try:
            response = requests.request("GET", url, headers={'cache-control': "no-cache"}, params=querystring)
            response_data = response.json()
            
            if response_data.get('return') == True:
                return JsonResponse({'status': 'success', 'message': 'OTP Sent to your phone!'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Phone verification is temporarily unavailable. Please use Google Login.'})
                
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': 'System is currently busy. Please try again later.'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})


def verify_phone_otp(request):
    """Verifies the code and logs the user in."""
    if request.method == 'POST':
        phone = request.POST.get('phone_number')
        user_otp = request.POST.get('otp')
        
        try:
            db_record = PhoneOTP.objects.get(phone_number=phone)
            
            if db_record.otp == user_otp:
                # Success! Get the user (or create a new account using their phone number)
                user, created = User.objects.get_or_create(username=phone)
                
                # Log them in securely
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                
                # Delete the OTP from the database so it cannot be reused
                db_record.delete()
                
                # Smart Redirect
                if user.is_superuser:
                    return JsonResponse({'status': 'success', 'redirect': '/management/command-center/'})
                else:
                    return JsonResponse({'status': 'success', 'redirect': '/'})
                
            else:
                return JsonResponse({'status': 'error', 'message': 'Invalid OTP code. Please try again.'})
                
        except PhoneOTP.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Session expired. Please request a new OTP.'})
            
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})

from django.core.mail import send_mail
from django.conf import settings

@login_required
def send_email_otp(request):
    """Generates and sends an OTP via Email using Django Sessions."""
    if request.method == 'POST':
        email = request.POST.get('email')
        if not email:
            return JsonResponse({'status': 'error', 'message': 'Please enter a valid email address.'})
        
        # Save email to the user model
        request.user.email = email
        request.user.save()

        # Generate a 6-digit OTP and store it securely in the user's session
        otp_code = str(random.randint(100000, 999999))
        request.session['email_otp'] = otp_code
        request.session['verifying_email'] = email
        
        try:
            # Send the email
            send_mail(
                subject='Rainbow Jobs - Email Verification',
                message=f'Hello,\n\nYour Rainbow Jobs email verification code is: {otp_code}\n\nPlease do not share this code.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False,
            )
            return JsonResponse({'status': 'success', 'message': 'OTP sent to your email!'})
        except Exception as e:
            print("Email Error:", e)
            return JsonResponse({'status': 'error', 'message': 'Failed to send email. Check SMTP settings.'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request.'})


@login_required
def confirm_email_otp(request):
    """Checks the Email OTP stored in the session."""
    if request.method == 'POST':
        user_otp = request.POST.get('otp')
        
        # Retrieve the OTP from the session
        session_otp = request.session.get('email_otp')
        
        if session_otp and str(session_otp) == str(user_otp):
            # Success! Mark as verified
            request.user.profile.is_email_verified = True
            request.user.profile.save()
            
            # Clear the session data
            del request.session['email_otp']
            del request.session['verifying_email']
            
            return JsonResponse({'status': 'success', 'message': 'Email verified successfully!'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Incorrect OTP code or session expired.'})
        

def public_profile(request, username):
    """Public read-only view for a candidate's portfolio."""
    # Find the user by their username, or return a 404 error if they don't exist
    candidate = get_object_or_404(User, username=username)
    
    return render(request, 'public_profile.html', {'candidate': candidate})