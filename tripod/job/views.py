from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

# from job.workflow_factory.workflow import WorkFlowBase
from job.models import Job, Work, Task
from job.forms import JobReqCreateForm, JobUpdateConfirmForm, AppointmentForm

from finance.models import PaymentHistory, Invoice
from finance.forms import (InvoiceUpdateForm, PaymentHistoryForm, ReceiptForm)

from tripod.utils import superuser_check, staff_check
# from tripod.tasks_lib.email import EmailClient


@login_required(login_url='company:staffLogin')
def staffJobHomePage(request):
    """
    home page for job page, where new requests, confirmed job and declined
    job will be shown
    """
    return render(request, 'staffs/job.html')


@login_required(login_url='company:staffLogin')
@user_passes_test(staff_check, login_url='permission_error')
def jobReqManagementPage(request):
    """
    job request management page
    """
    query = request.GET.get('q')
    jobs = Job.objects.filter(status='req')
    if query is not None:
        lookup = Q(job_name__icontains=query) | Q(
            primary_client__first_name=query) | Q(
                primary_client__last_name=query)

        jobs = jobs.filter(lookup)
    context = {'reqJobs': jobs}

    return render(request, 'jobManagement/jobReqManagement.html', context)


@login_required(login_url='company:staffLogin')
@user_passes_test(staff_check, login_url='permission_error')
def jobDecManagementPage(request):
    """
    declined job management page
    """
    jobs = Job.objects.filter(status='dec')
    query = request.GET.get('q')
    if query is not None:
        lookup = Q(job_name__icontains=query) | Q(
            primary_client__first_name=query) | Q(
                primary_client__last_name=query)
        jobs = jobs.filter(lookup)
    context = {'reqJobs': jobs}

    return render(request, 'jobManagement/jobDecManagement.html', context)


@login_required(login_url="company:staffLogin")
@user_passes_test(superuser_check, login_url='permission_error')
def jobReqAddPage(request):
    """
    Adding a new job request
    """
    form = JobReqCreateForm(userObj=None)
    if request.method == "POST":
        form = JobReqCreateForm(request.POST, userObj=request.user)
        if form.is_valid():
            obj = form.save()
            messages.success(request, f'Job request was created for {obj}')
            return redirect('job:jobReqManagementPage')
        else:
            messages.error(request, 'Invalid form submission')

    context = {'form': form}
    return render(request, 'jobManagement/jobReqAdd.html', context)


@login_required(login_url="company:staffLogin")
@user_passes_test(superuser_check, login_url='permission_error')
def jobChangeReqToJob(request, pk):
    """
    Change job request to Job
    """
    job = Job.objects.get(pk=pk)
    form = JobUpdateConfirmForm(instance=job, userObj=None, operation=None)

    if request.method == 'POST':
        form = JobUpdateConfirmForm(request.POST,
                                    instance=job,
                                    userObj=request.user,
                                    operation='confirming Job')
        if form.is_valid():
            obj = form.save()
            messages.success(request, f'Job is confirmed and updated {obj}')
            return redirect('job:jobPage', job.id)
        else:
            messages.error(request, 'Invalid form submission')

    context = {'form': form, 'job': job}
    return render(request, 'jobManagement/jobConfirmPage.html', context)


@login_required(login_url='company:staffLogin')
@user_passes_test(staff_check, login_url='permission_error')
def jobManagementPage(request):
    """
    job management page
    """
    jobs = Job.objects.filter(status='job')
    query = request.GET.get('q')
    if query is not None:
        lookup = Q(job_name__icontains=query) | Q(
            primary_client__first_name=query) | Q(
                primary_client__last_name=query)
        jobs = jobs.filter(lookup)
    context = {'jobs': jobs}

    return render(request, 'jobManagement/jobManagement.html', context)


@login_required(login_url="company:staffLogin")
@user_passes_test(superuser_check, login_url='permission_error')
def jobUpdateJob(request, pk):
    """
    Change job request to Job
    """
    job = Job.objects.get(pk=pk)
    form = JobUpdateConfirmForm(instance=job, userObj=None, operation=None)

    if request.method == 'POST':
        form = JobUpdateConfirmForm(request.POST,
                                    instance=job,
                                    userObj=request.user,
                                    operation='updating')
        if form.is_valid():
            obj = form.save()
            messages.success(request, f'Job {obj} successfully updated')
            return redirect('job:jobPage', job.id)
        else:
            messages.error(request, 'Invalid form submission')

    context = {'form': form, 'job': job}
    return render(request, 'jobManagement/jobUpdatePage.html', context)


@login_required(login_url='company:staffLogin')
@user_passes_test(staff_check, login_url='permission_error')
def jobPage(request, pk):
    """
    job page
    """
    job = Job.objects.get(pk=pk)
    invoice = job.invoice
    payment_history = invoice.paymenthistory_set.all()
    works = Work.objects.filter(job=job).order_by('work_order')
    context = {
        'job': job,
        'works': works,
        'invoice': invoice,
        'pyHistory': payment_history
    }

    return render(request, 'jobManagement/job.html', context)


@login_required(login_url='company:staffLogin')
@user_passes_test(staff_check, login_url='permission_error')
def processTask(request, pk):
    """processing and completing the task from admin or business side"""
    task = Task.objects.get(pk=pk)
    work = task.work
    job = work.job

    # making sure that task is process correctly
    try:
        task.process_task(request.user)
        messages.success(request, f'Task {task} is successfully processed')
        return redirect('job:jobPage', job.id)
    except Exception as e:
        messages.error(request,
                       f'Exception {e} occured while processing the task')
        return redirect('job:jobPage', job.id)


@login_required(login_url='company:staffLogin')
@user_passes_test(staff_check, login_url='permission_error')
def completeTask(request, pk):
    """complete task from the user side"""
    task = Task.objects.get(pk=pk)
    job = task.get_job()
    task.user_completed = task.update_user_completed()
    task.completed = task.update_task_completed()
    task.save()
    messages.success(request, f'Task {task} is successfully completed')
    return redirect('job:jobPage', job.id)


@login_required(login_url='company:staffLogin')
@user_passes_test(staff_check, login_url='permission_error')
def appointmentPage(request, pk):
    task = Task.objects.get(pk=pk)
    job = task.get_job()
    app = task.appointment

    if app:
        form = AppointmentForm(instance=app)
    else:
        form = AppointmentForm()

    if request.method == 'POST':
        if app:
            form = AppointmentForm(request.POST, instance=app)
        else:
            form = AppointmentForm(request.POST)

        if form.is_valid():
            appObj = form.save()
            task.appointment = appObj
            task.save()
            messages.success(request, f'Appointment successfully created')
        else:
            messages.error(request, 'Invalid form submission')

        return redirect('job:jobPage', job.id)

    context = {'form': form, 'task': task, 'job': job}
    return render(request, 'appManagement/app.html', context)


@login_required(login_url='company:staffLogin')
@user_passes_test(superuser_check, login_url='permission_error')
def updateInvoice(request, pk):
    """Add discount if wanted to notes before sharing invoice"""
    invoice = Invoice.objects.get(pk=pk)
    form = InvoiceUpdateForm(instance=invoice)

    if request.method == 'POST':
        form = InvoiceUpdateForm(request.POST, instance=invoice)
        if form.is_valid():
            invoice = form.save(commit=False)
            if invoice.discount:
                invoice.total_price = invoice.price - (invoice.price *
                                                       invoice.discount)
            invoice.save()
            messages.success(request, f'Invoice is updated successfully')
            return redirect('company:invoiceDetail', invoice.id)
        else:
            messages.error(request, 'Invalid form submission')

    context = {'form': form, 'invoice': invoice, 'job': invoice.job}
    return render(request, 'jobManagement/invoice.html', context)


@login_required(login_url='company:staffLogin')
@user_passes_test(staff_check, login_url='permission_error')
def invoicePage(request, pk):
    """displaying invoice page"""
    job = Job.objects.get(pk=pk)
    invoice = job.invoice

    context = {'invoice': invoice}

    return render(request, 'jobManagement/invoicePage.html', context)


@login_required(login_url='company:staffLogin')
@user_passes_test(staff_check, login_url='permission_error')
def questPage(request, pk):
    """displaying invoice page"""
    job = Job.objects.get(pk=pk)
    tasks = job.get_user_quest_tasks()
    questionnaires = [task.job_quest for task in tasks]

    context = {
        'questionnaires': questionnaires,
        'job': job,
    }

    return render(request, 'jobManagement/questPage.html', context)


@login_required(login_url='company:staffLogin')
@user_passes_test(staff_check, login_url='permission_error')
def addPayHistoryPage(request, pk):
    """adding payment history"""
    job = Job.objects.get(pk=pk)
    invoice = job.invoice
    form = PaymentHistoryForm(invoice=invoice)

    if request.method == 'POST':
        form = PaymentHistoryForm(request.POST, invoice=invoice)
        try:
            if form.is_valid():
                ph = form.save(commit=False)
                ph.invoice = invoice
                obj = ph.save()
                messages.success(request,
                                 f'Payment record successfully created')
                return redirect('job:jobPage', job.id)
            else:
                messages.error(request, 'Invalid form submission')
        except Exception as e:
            messages.error(request, f'{e}')

    context = {'form': form, 'invoice': invoice}
    return render(request, 'jobManagement/PayHistory.html', context)


@login_required(login_url='company:staffLogin')
@user_passes_test(staff_check, login_url='permission_error')
def updatePayHistoryPage(request, pk):
    """adding payment history"""
    ph = PaymentHistory.objects.get(pk=pk)
    job = ph.invoice.job
    form = PaymentHistoryForm(instance=ph)

    if request.method == 'POST':
        form = PaymentHistoryForm(request.POST, instance=ph)
        if form.is_valid():
            ph = form.save()
            messages.success(request, f'Payment record successfully updated')
            return redirect('job:jobPage', job.id)
        else:
            messages.error(request, 'Invalid form submission')

    context = {'form': form}
    return render(request, 'jobManagement/PayHistory.html', context)
