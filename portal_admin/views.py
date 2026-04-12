from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from jobs.models import Job, Category # Import your new models!

# Security check: Is the user an admin?
def is_admin(user):
    return user.is_authenticated and user.is_superuser

@login_required(login_url='login')
@user_passes_test(is_admin, login_url='home')
def dashboard_view(request):
    """Renders the main admin dashboard with platform statistics."""
    context = {
        'total_users': User.objects.count(),
        'categories': Category.objects.all(), # Send categories to the Add Job Modal
        'active_jobs': Job.objects.filter(is_active=True).count(),
        'jobs_list': Job.objects.all().order_by('-created_at')[:10], # Show 10 most recent jobs
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