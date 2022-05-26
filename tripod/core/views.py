from django.shortcuts import redirect, render

from django.contrib import messages
from django.contrib.auth import (authenticate, login, logout,
                                 update_session_auth_hash)
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import get_user_model
from django.db.models import Q

from tripod.utils import superuser_check, force_password_change_check

from job.models import Job, JobContract, JobQuestionnaire, Task, Work
from job.utils import get_job_completed_percentage

from finance.models import Invoice
from finance.utils import register_invoice_data_for_job

from blog.forms import CustomerCreationForm as BlogCustomerCreationForm

from core.forms import (CustomUserCreationForm, JobUserUpdateForm,
                        CustomUserChangeForm, QuestionnaireUpdate,
                        JobReqCreatedForm, JobPackageUpdate)
from core.models import Company

from company.models import PackageLinkProduct


def redirect_to_change_password(user):
    if force_password_change_check(user):
        redirect('core:changePassword')


@login_required
def changePassword(request):
    """
    Account registration view function for customers or users
    using email, username and password
    """
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            user.force_password_change = False
            user.password_change_code = ''
            user.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request,
                             'Your password was successfully updated!')
            return redirect('core:customerHome')
        else:
            messages.error(request, 'Invalid form submission')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/change_password.html', {'form': form})


def loginPage(request):
    """
    Login view function for customers or users using email and password
    """
    if request.user.is_authenticated:
        return redirect('core:customerHome')
    else:
        if request.method == "POST":
            email = request.POST.get('email')
            password = request.POST.get('password')

            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                if user.force_password_change:
                    messages.warning(request, 'Change password!')
                    return redirect('core:changePassword')
                else:
                    messages.success(request, 'login success')
                    return redirect('core:customerHome')
            else:
                messages.info(request, 'Username or password incorrect')

        context = {}
        return render(request, 'accounts/login.html', context)


@login_required(login_url='core:login')
def logoutPage(request):
    """
    Logout view function for customers or user
    which redirects back to home
    """
    logout(request)
    messages.info(request, 'Successfully logged out')
    return redirect('core:login')


def home(request):
    """
    customers or users home view function
    """
    reg_form = BlogCustomerCreationForm()
    context = {'reg_form': reg_form}
    context['user'] = request.user
    return render(request, 'accounts/home.html', context)


@login_required(login_url='core:login')
def customerHome(request):
    """home page of after customer logs in"""
    redirect_to_change_password(request.user)
    jobs = Job.objects.filter(primary_client=request.user)
    context = {'user': request.user, 'jobs': jobs}
    return render(request, 'customer/home.html', context)


@login_required(login_url='core:login')
@user_passes_test(force_password_change_check, login_url='core:changePassword')
def jobRequests(request):
    """Job requests information page"""
    query = request.GET.get('q')
    jobs = Job.objects.filter(primary_client=request.user).filter(status='req')
    if query is not None:
        lookup = Q(job_name__icontains=query)
        jobs = jobs.filter(lookup)
    context = {'user': request.user, 'jobs': jobs, 'jobStatus': 'req'}
    return render(request, 'customer/job/jobTable.html', context)


@login_required(login_url='core:login')
@user_passes_test(force_password_change_check, login_url='core:changePassword')
def jobsConfirmed(request):
    """Confimed jobs information page"""
    query = request.GET.get('q')
    jobs = Job.objects.filter(primary_client=request.user).filter(status='job')
    if query is not None:
        lookup = Q(job_name__icontains=query)
        jobs = jobs.filter(lookup)
    context = {'user': request.user, 'jobs': jobs, 'jobStatus': 'conf'}
    return render(request, 'customer/job/jobTable.html', context)


@login_required(login_url='core:login')
@user_passes_test(force_password_change_check, login_url='core:changePassword')
def jobsDeclined(request):
    """declined jobs info"""
    query = request.GET.get('q')
    jobs = Job.objects.filter(primary_client=request.user).filter(status='dec')
    if query is not None:
        lookup = Q(job_name__icontain=query)
        jobs = jobs.filter(lookup)
    context = {'user': request.user, 'jobs': jobs, 'jobStatus': 'decl'}
    return render(request, 'customer/job/jobTable.html', context)


@login_required(login_url='core:login')
@user_passes_test(force_password_change_check, login_url='core:changePassword')
def jobPage(request, pk):
    """
    shows job and its content
    """
    job = Job.objects.get(pk=pk)
    works = Work.objects.filter(job=job).order_by('work_order')
    if job.primary_client != request.user:
        redirect('error')
    try:
        jobContract = JobContract.objects.get(job=job)
    except JobContract.DoesNotExist:
        jobContract = None

    try:
        job_quest = JobQuestionnaire.objects.get(job=job)
    except JobQuestionnaire.DoesNotExist:
        job_quest = None

    try:
        invoice = Invoice.objects.get(job=job)
        if invoice.total_price == 0:
            invoice = None
    except Invoice.DoesNotExist:
        invoice = None

    context = {
        'job': job,
        'job_completion': get_job_completed_percentage(job),
        'contract_tasks': job.get_user_contract_tasks(),
        'quest_tasks': job.get_user_quest_tasks(),
        'invoice': invoice,
        'app_tasks': job.get_user_appointment_tasks(),
        'works': works
    }

    return render(request, 'customer/job/job.html', context)


@login_required(login_url='core:login')
@user_passes_test(force_password_change_check, login_url='core:changePassword')
def jobUpdate(request, pk):
    """job updating form of user"""
    job = Job.objects.get(pk=pk)
    package = job.package
    form = JobUserUpdateForm(instance=job)

    if request.method == 'POST':
        form = JobUserUpdateForm(request.POST, instance=job)
        if form.is_valid():
            job.job_name = form.cleaned_data['job_name']
            job.description = form.cleaned_data['description']
            job.venue = form.cleaned_data['venue']
            job.venue_notes = form.cleaned_data['venue_notes']
            job.start_date = form.cleaned_data['start_date']
            job.end_date = form.cleaned_data['end_date']
            job.start_time = form.cleaned_data['start_time']
            job.end_time = form.cleaned_data['end_time']
            job.package = package
            job.changed_by = request.user
            job.save()
            if job.package:
                register_invoice_data_for_job(job, package=True)
            else:
                register_invoice_data_for_job(job, package=False)
            messages.success(request, f'Job {job} successfully updated')
            return redirect('core:jobPage', job.id)
        else:
            messages.error(request, 'Invalid form submission')

    context = {'form': form, 'job': job}
    return render(request, 'customer/job/updateJob.html', context)


@login_required(login_url='core:login')
@user_passes_test(force_password_change_check, login_url='core:changePassword')
def jobUpdatePackage(request, pk):
    """
    user updating the package info
    """
    job = Job.objects.get(pk=pk)
    form = JobPackageUpdate(instance=job)

    if request.method == "POST":
        form = JobPackageUpdate(request.POST, instance=job)
        if form.is_valid():
            print(job.venue)
            job.package = form.cleaned_data['package']
            job.changed_by = request.user
            job.save()
            if job.package:
                register_invoice_data_for_job(job, package=True)
            else:
                register_invoice_data_for_job(job, package=False)
            messages.success(request, f'Job {job} successfully updated')
            return redirect('core:jobPage', job.id)
        else:
            messages.error(request, 'Invalid form submission')

    context = {'form': form, 'job': job}
    return render(request, 'customer/job/updateJobPackage.html', context)


@login_required(login_url='core:login')
@user_passes_test(force_password_change_check, login_url='core:changePassword')
def completeTask(request, pk):
    """processing task - user completion"""
    task = Task.objects.get(pk=pk)
    job = task.get_job()
    task.user_completed = 'uc'
    task.save()
    messages.success(request, f'Task {task} successfully sent')
    return redirect('core:jobPage', job.id)


@login_required(login_url='core:login')
@user_passes_test(force_password_change_check, login_url='core:changePassword')
def contractPage(request, pk):
    """showing contract for user"""
    task = Task.objects.get(pk=pk)
    jobContract = task.job_contract
    context = {'jobContract': jobContract}

    return render(request, 'customer/job/contractPage.html', context)


@login_required(login_url='core:login')
@user_passes_test(force_password_change_check, login_url='core:changePassword')
def invoicePage(request, pk):
    """showing contract for user"""
    company = Company.objects.filter(active=True).first()
    invoice = Invoice.objects.get(pk=pk)
    pkgLink = PackageLinkProduct.objects.filter(package=invoice.job.package)
    context = {'invoice': invoice, 'pkgLink': pkgLink, 'company': company}

    return render(request, 'customer/job/invoicePage.html', context)


@login_required(login_url='core:login')
@user_passes_test(force_password_change_check, login_url='core:changePassword')
def updateQuestForm(request, pk):
    """updating quest form"""
    task = Task.objects.get(pk=pk)
    job = task.get_job()
    quest = task.quest_template
    job_quest = task.job_quest
    form = QuestionnaireUpdate(instance=job_quest)

    if request.method == 'POST':
        form = QuestionnaireUpdate(request.POST, instance=job_quest)
        if form.is_valid():
            form.save()
            task.user_completed = 'uc'
            task.save()
            messages.success(request, f'Questionnaire updated and sent')
            return redirect('core:jobPage', job.id)
        else:
            messages.error(request, f'invalid submission')

    context = {'form': form, 'quest': quest}
    return render(request, 'customer/job/quest.html', context)


@login_required(login_url='core:login')
@user_passes_test(force_password_change_check, login_url='core:changePassword')
def jobReqAddPage(request):
    """
    Creating a job request
    """
    form = JobReqCreatedForm(userObj=None)
    if request.method == "POST":
        form = JobReqCreatedForm(request.POST, userObj=request.user)
        if form.is_valid():
            job = form.save()
            messages.success(request,
                             f'Job request {job} successfully created')
            return redirect('core:jobPage', job.id)
        else:
            messages.error(request, f'Invalid form submission')

    context = {'form': form}
    return render(request, 'customer/job/jobReqAdd.html', context)


@login_required(login_url='core:login')
@user_passes_test(force_password_change_check, login_url='core:changePassword')
def updateUserProfile(request, pk):
    """
    updating user profile
    """
    user = get_user_model().objects.get(pk=pk)
    form = CustomUserChangeForm(instance=user)
    context = {'form': form, 'user': user}

    if request.method == "POST":
        form = CustomUserChangeForm(request.POST or None, instance=user)
        if form.is_valid():
            user.email = form.cleaned_data['email']
            user.username = form.cleaned_data['username']
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.gender = form.cleaned_data['gender']
            user.contact_number = form.cleaned_data['contact_number']
            user.contact_number_2 = form.cleaned_data['contact_number_2']
            user.address = form.cleaned_data['address']
            user.address_2 = form.cleaned_data['address_2']
            user.city = form.cleaned_data['city']
            user.province = form.cleaned_data['province']
            user.country = form.cleaned_data['country']
            user.is_client = True
            user.is_staff = False
            user.is_active = True
            user.is_superuser = False
            user.save()
            messages.success(request, f"Successfully updated the profile")
            return redirect('core:customerHome')
        else:
            messages.error(request, form.errors.as_text())
            return render(request, 'customer/updateUser.html', context)

    return render(request, 'customer/updateUser.html', context)
