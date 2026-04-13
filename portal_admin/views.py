from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from jobs.models import Job, Category,JobApplication # Import your new models!

# Security check: Is the user an admin?
def is_admin(user):
    return user.is_authenticated and user.is_superuser

@login_required(login_url='login')
@user_passes_test(is_admin, login_url='home')
def dashboard_view(request):
    """Renders the main admin dashboard with platform statistics and applications."""
    context = {
        'total_users': User.objects.count(),
        'categories': Category.objects.all(), # Send categories to the Add Job Modal
        'active_jobs': Job.objects.filter(is_active=True).count(),
        'jobs_list': Job.objects.all().order_by('-created_at')[:10], # Show 10 most recent jobs
        
        # --- NEW: ADDING APPLICATIONS TO YOUR DASHBOARD ---
        'total_applications': JobApplication.objects.count(),
        'applications': JobApplication.objects.all().order_by('-applied_at')[:15], 
    }
    return render(request, 'admin/admin_dashboard.html', context)


@login_required(login_url='login')
@user_passes_test(is_admin, login_url='home')
def add_job(request):
    """Catches the form submission and saves a new Job to the database."""
    if request.method == 'POST':
        # 1. Get the category instance from the ID submitted in the form
        cat_id = request.POST.get('category')
        category_instance = Category.objects.get(id=cat_id) if cat_id else None

        # 2. Check if the "Urgent" checkbox was ticked (checkboxes return 'on' if ticked)
        is_urgent = request.POST.get('is_urgent') == 'on'

        # 3. Create and save the new Job
        Job.objects.create(
            title=request.POST.get('title'),
            category=category_instance,
            company_name=request.POST.get('company_name'),
            location=request.POST.get('location'),
            salary=request.POST.get('salary'),
            gender=request.POST.get('gender', 'Any'), # Default to 'Any' if left blank
            timing=request.POST.get('timing'),
            experience=request.POST.get('experience'),
            description=request.POST.get('description'),
            requirements=request.POST.get('requirements'),
            benefits=request.POST.get('benefits'),
            contact_info=request.POST.get('contact_info'),
            is_urgent=is_urgent,
            posted_by=request.user # Automatically logs which admin posted it
        )
        
        messages.success(request, "New executive job successfully published!")
        return redirect('admin_dashboard')
        
    return redirect('admin_dashboard')

@login_required(login_url='login')
@user_passes_test(is_admin, login_url='home')
def add_category(request):
    """Catches the form submission and saves a new Category to the database."""
    if request.method == 'POST':
        cat_name = request.POST.get('name')
        cat_desc = request.POST.get('description', '')

        # Check if it already exists to prevent database errors
        if Category.objects.filter(name__iexact=cat_name).exists():
            messages.error(request, f"Category '{cat_name}' already exists.")
        else:
            Category.objects.create(name=cat_name, description=cat_desc)
            messages.success(request, f"Category '{cat_name}' successfully added!")
            
    return redirect('admin_dashboard')

@login_required(login_url='login')
@user_passes_test(is_admin, login_url='home')
def all_applications(request):
    """Renders the Applicant Tracking & Onboarding System."""
    # Fetch all applications, newest first
    applications = JobApplication.objects.all().order_by('-applied_at')
    
    context = {
        'applications': applications,
    }
    return render(request, 'admin/admin_applications.html', context)

@login_required(login_url='login')
@user_passes_test(is_admin, login_url='home')
def update_application_status(request, app_id):
    """Securely updates the status and private notes of an application."""
    if request.method == 'POST':
        app = get_object_or_404(JobApplication, id=app_id)
        
        # Get the submitted data
        new_status = request.POST.get('status')
        new_notes = request.POST.get('admin_notes')
        new_rating = request.POST.get('rating', 0) # Defaults to 0 if not provided
        
        # Save the notes and rating
        app.admin_notes = new_notes
        app.rating = int(new_rating)
        
        # Security check: Ensure the status is valid
        valid_statuses = dict(JobApplication.STATUS_CHOICES).keys()
        if new_status in valid_statuses:
            app.status = new_status
            
        app.save()
        messages.success(request, f"Candidate profile for {app.applicant_name} updated successfully.")
            
    return redirect('all_applications')

@login_required(login_url='login')
@user_passes_test(is_admin, login_url='home')
def manage_jobs(request):
    """Renders a table of all jobs for the admin to manage, with category filtering."""
    jobs = Job.objects.all().order_by('-created_at')
    categories = Category.objects.all() # Fetch categories for the filter tabs
    
    context = {
        'jobs': jobs,
        'categories': categories
    }
    return render(request, 'admin/admin_manage_jobs.html', context)

@login_required(login_url='login')
@user_passes_test(is_admin, login_url='home')
def toggle_job_status(request, job_id):
    """Instantly hides or shows a job on the public homepage."""
    job = get_object_or_404(Job, id=job_id)
    job.is_active = not job.is_active # Flips True to False, or False to True
    job.save()
    
    status_msg = "VISIBLE" if job.is_active else "HIDDEN"
    messages.success(request, f"'{job.title}' is now {status_msg} on the public site.")
    return redirect('manage_jobs')

@login_required(login_url='login')
@user_passes_test(is_admin, login_url='home')
def edit_job(request, job_id):
    """Renders the edit form and saves changes to a specific job."""
    job = get_object_or_404(Job, id=job_id)
    categories = Category.objects.all()

    if request.method == 'POST':
        cat_id = request.POST.get('category')
        category_instance = Category.objects.get(id=cat_id) if cat_id else None

        # Update the job fields
        job.title = request.POST.get('title')
        job.category = category_instance
        job.company_name = request.POST.get('company_name')
        job.location = request.POST.get('location')
        job.salary = request.POST.get('salary')
        job.gender = request.POST.get('gender')
        job.timing = request.POST.get('timing')
        job.experience = request.POST.get('experience')
        job.description = request.POST.get('description')
        job.requirements = request.POST.get('requirements')
        job.benefits = request.POST.get('benefits')
        job.contact_info = request.POST.get('contact_info')
        job.is_urgent = request.POST.get('is_urgent') == 'on'

        job.save()
        messages.success(request, f"Changes to '{job.title}' saved successfully.")
        return redirect('manage_jobs')

    context = {'job': job, 'categories': categories}
    return render(request, 'admin/admin_edit_job.html', context)