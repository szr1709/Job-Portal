from django.shortcuts import render,redirect
from JobPortal.models import *
from JobPortal.forms import *
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q

def register_page(request):
    if request.method == 'POST':
        form_data = RegistrationForm(request.POST)
        if form_data.is_valid():
            form_data.save()
            messages.success(request, 'Registration Successsfull')
            return redirect('login_page')
    else:
        form_data = RegistrationForm()
    context={
        'form_data' : form_data,
        'title' : 'Register Page', 
        'form_name' : 'Registration Form',
        'form_btn' : 'Register'
    }
    return render(request, 'master/base-form.html', context)

def login_page(request):
    if request.method == 'POST':
        form_data = AuthenticationForm(request, data=request.POST)
        if form_data.is_valid():
            user = form_data.get_user()
            if user:
                login(request, user)
                messages.success(request, 'Login Successfull')
                return redirect('dashboard_page')
            else:
                messages.error(request, 'Login Un_successfull')
    else:
        form_data = AuthenticationForm()

    context = {
    'form_data' : form_data,
    'title' : 'Login Page', 
    'form_name' : 'Login Form',
    'form_btn' : 'Login'
    }
    return render(request, 'master/base-form.html', context)

@login_required
def dashboard_page(request):
    if request.user.user_type == 'Recruiter':
            return render(request, 'dashboard.html', {'job_data': JobPostModel.objects.all()})

    try:
        seeker_skill = request.user.seeker_profile.skills_set
    except:
        messages.error(request, 'Please update your profile first.')
        return redirect('update_profile_view')

    job_data = JobPostModel.objects.none()

    if seeker_skill:
        for skill in seeker_skill.split(','):
            job_data |= JobPostModel.objects.filter(
                skills_set__icontains=skill.strip()
            )

    context = {
        "job_data": job_data
    }

    return render(request, 'dashboard.html', context)

@login_required
def logout_page(request):
    logout(request)
    messages.success(request, 'Logged Out')
    return redirect('login_page')


@login_required
def profile_view(request):

    return render(request, 'profile.html')

@login_required
def update_profile_view(request):
    current_user = request.user
    if current_user.user_type == 'Recruiter':
        try:
            profile_data = RecruiterProfileModel.objects.get(recruiter = current_user)
        except:
            profile_data = None

        if request.method == 'POST':
            form_data = RecruiterProfileUpdateForm(request.POST, request.FILES, instance= profile_data)
            if form_data.is_valid():
                data = form_data.save(commit=False)
                data.recruiter = current_user
                data.save()
                messages.success(request, 'Profile Updated Successfully')
                return redirect('profile_view')
        form_data = RecruiterProfileUpdateForm(instance= profile_data)
    else:
        try:
            profile_data = SeekerProfileModel.objects.get(seeker = current_user)
        except:
            profile_data = None
        if request.method == 'POST':
            form_data = SeekerProfileUpdateForm(request.POST, request.FILES, instance= profile_data)
            if form_data.is_valid():
                data = form_data.save(commit=False)
                data.seeker = current_user
                data.save()
                messages.success(request, 'Profile Updated Successfully')
                return redirect('profile_view')
        form_data = SeekerProfileUpdateForm(instance= profile_data)
         
    context = {
    'form_data' : form_data,
    'title' : 'Update Profile Info', 
    'form_name' : 'Update Profile Form',
    'form_btn' : 'Update Profile'
    }
    return render(request, 'master/base-form.html', context)

@login_required
def post_job_view(request):
    if request.method == 'POST':
        form_data = JobPostForm(request.POST, request.FILES)
        if form_data.is_valid():
            data = form_data.save(commit=False)
            data.posted_by = request.user.recruiter_profile
            data.save()
            messages.success(request, 'Job Posted Successfully')
            return redirect('browse_job')
        
    form_data = JobPostForm()
    context = {
    'form_data' : form_data,
    'title' : 'Post Job Page', 
    'form_name' : 'Post Job Info Form',
    'form_btn' : 'Post Job'
    }
    return render(request, 'master/base-form.html', context)


def browse_job(request):
    current_user = request.user
    print(current_user)
    search_query = request.GET.get('search_query')

    job_data = JobPostModel.objects.all()
    print("browse job: ", job_data)

    if  current_user.is_authenticated:
        print("sdlfjsdlfka")
        if current_user.user_type == 'Recruiter':
            try:
                job_data = job_data.filter(posted_by = current_user.recruiter_profile)
            except:
                messages.error(request, 'Please, Update your profile first.')
                return redirect('update_profile_view')
    if search_query:
        job_data = job_data.filter(
            Q(title__icontains = search_query) |
            Q(category__name__icontains = search_query) |
            Q(posted_by__company_name__icontains = search_query)
        )
    context = {
        'job_data': job_data
    }
    return render(request, 'browse-job.html', context)

def job_detail_view(request, id):
    job = JobPostModel.objects.get(id=id)

    context = {
        'job': job
    }

    return render(request, 'job-detail.html', context)


@login_required
def update_post_job_view(request, id):
    try:
        recruiter_data = request.user.recruiter_profile
        job = JobPostModel.objects.get(id=id, )
    except:
        messages.error(request, 'Please, Update Your Profile Frist!')
        return redirect('update_profile_view')
    
    if request.method == 'POST':
        form_data = JobPostForm(request.POST, request.FILES, instance= job)
        if form_data.is_valid():
            data = form_data.save(commit=False)
            data.posted_by = recruiter_data
            data.save()
            messages.success(request, 'Job Update Successfully')
            return redirect('browse_job')
    else:
        form_data = JobPostForm(instance= job)

        
    context = {
            'form_data' : form_data,
            'form_name' : 'Update Job Post Form',
            'form_btn' : 'Update Job',
            'title' : 'Update Job page'
        }
    return render(request, 'master/base-form.html', context)

@login_required
def delete_post_job_view(request, id):
    try:
        JobPostModel.objects.get(id=id).delete()
        messages.success(request, 'Job Deleted Successfully')
        return redirect('browse_job')
    except:
        messages.error(request, 'Job Not Found!')
        return redirect('browse_job')
  

@login_required
def apply_job_view(request, id):
    try:
        seeker_profile = request.user.seeker_profile
        job = JobPostModel.objects.get(id=id)
    except:
        messages.error(request, 'Please, Update your profile first.')
        return redirect('update_profile_view')
    # ✅ prevent duplicate application
    if ApplyJobModel.objects.filter(
        applied_by=seeker_profile,
        applied_job=job
    ).exists():
        messages.error(request, "You already applied for this job!")
        return redirect('browse_job')
    
    if request.method == 'POST':
        form_data = ApplyJobForm(request.POST, request.FILES)
        if form_data.is_valid():
            data = form_data.save(commit=False)
            data.applied_by = seeker_profile
            data.applied_job = job
            data.save()
            messages.success(request, 'Application submit successfully.')
            return redirect('browse_job')

    form_data = ApplyJobForm()
    context = {
        'form_data': form_data,
        'title': 'Apply Job Page',
        'form_title': 'Apply Job Info Form',
        'form_btn': 'Apply',
    }
    return render(request, 'master/base-form.html', context)
def my_application(request):
    try:
        my_application = ApplyJobModel.objects.filter(applied_by = request.user.seeker_profile)
    except:
        messages.error(request, 'Please, Update your profile first.')
        return redirect('update_profile_view')
    context = {
        'application_list': my_application,
        'title': 'My Application Page',
        'form_title': 'Apply Job Info Form',
        'form_btn': 'Apply',
    }
    return render(request, 'my-applications.html',context)

def candidate_list_view(request, id):

    job_data = JobPostModel.objects.get(id=id)
    candidate_data = ApplyJobModel.objects.filter(applied_job=job_data)
    if request.method == "POST":
        candidate_id = request.POST.get('candidate_id')
        status = request.POST.get('status')
        candidate = ApplyJobModel.objects.get(id=candidate_id)
        candidate.status = status
        candidate.save()
        return redirect('candidate_list_view', id=id)

    context = {
        'candidate_data': candidate_data,
        'job_data': job_data,
        'title': 'Candidate List Page',
    }
    return render(request,'candidate-list.html',context)