from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test

from job.workflow_factory.workflow import WorkFlowBase
from job.models import Job, Work, Task
from job.forms import JobReqCreateForm, JobUpdateConfirmForm

from finance.utils import prepare_invoice_sharing

from tripod.utils import superuser_check
from tripod.tasks_lib.email import EmailClient


@login_required(login_url='company:staffLogin')
def staffJobHomePage(request):
    """
    home page for job page, where new requests, confirmed job and declined
    job will be shown
    """
    return render(request, 'staffs/job.html')


@login_required(login_url='company:staffLogin')
@user_passes_test(superuser_check)
def jobReqManagementPage(request):
    """
    job request management page
    """
    jobs = Job.objects.filter(status='req')
    context = {'reqJobs': jobs}

    return render(
        request, 'jobManagement/jobReqManagement.html', context)


@login_required(login_url="company:staffLogin")
@user_passes_test(superuser_check)
def jobReqAddPage(request):
    """
    Adding a new job request
    """
    form = JobReqCreateForm(userObj=None)
    if request.method == "POST":
        form = JobReqCreateForm(
            request.POST, userObj=request.user)
        if form.is_valid():
            form.save()
        return redirect('job:jobReqManagementPage')

    context = {'form': form}
    return render(request, 'jobManagement/jobReqAdd.html', context)


@login_required(login_url="company:staffLogin")
@user_passes_test(superuser_check)
def jobChangeReqToJob(request, pk):
    """
    Change job request to Job
    """
    job = Job.objects.get(pk=pk)
    form = JobUpdateConfirmForm(instance=job, userObj=None, operation=None)

    if request.method == 'POST':
        form = JobUpdateConfirmForm(
            request.POST, instance=job,
            userObj=request.user, operation='confirming Job'
        )
        if form.is_valid():
            form.save()
        return redirect('job:jobPage', job.id)

    context = {'form': form, 'job': job}
    return render(
        request, 'jobManagement/jobConfirmPage.html', context)


@login_required(login_url='company:staffLogin')
@user_passes_test(superuser_check)
def jobManagementPage(request):
    """
    job management page
    """
    jobs = Job.objects.filter(status='job')
    context = {'jobs': jobs}

    return render(
        request, 'jobManagement/jobManagement.html', context)


@login_required(login_url="company:staffLogin")
@user_passes_test(superuser_check)
def jobUpdateJob(request, pk):
    """
    Change job request to Job
    """
    job = Job.objects.get(pk=pk)
    form = JobUpdateConfirmForm(instance=job, userObj=None, operation=None)

    if request.method == 'POST':
        form = JobUpdateConfirmForm(
            request.POST, instance=job,
            userObj=request.user, operation='updating'
        )
        if form.is_valid():
            form.save()
        return redirect('job:jobPage', job.id)

    context = {'form': form, 'job': job}
    return render(
        request, 'jobManagement/jobUpdatePage.html', context)


@login_required(login_url='company:staffLogin')
@user_passes_test(superuser_check)
def jobPage(request, pk):
    """
    job page
    """
    job = Job.objects.get(pk=pk)
    works = Work.objects.filter(job=job)
    context = {'job': job, 'works': works}

    return render(
        request, 'jobManagement/job.html', context)


def process_work(work, user, invoice):
    # TODO -  has to develop this further
    tasks = Task.objects.filter(work=work)
    for task in tasks:
        if task.task_type == 'em':
            print('sending email')
            task.send_email(user)
            # task.completed = True
            # task.save()
        elif task.task_type == 'cn':
            print('sending contract')
            invoice_content = prepare_invoice_sharing(invoice)
            task.send_contract_and_invoice(user, invoice_content)
        elif task.task_type == 'qn':
            print('sending question')
        else:
            print('completing task')
            # task.completed = True
            # task.save()


@login_required(login_url='company:staffLogin')
@user_passes_test(superuser_check)
def completeWork(request, pk):
    work = Work.objects.get(pk=pk)
    job_id = work.job.id
    invoice = work.job.invoice
    try:
        process_work(work, request.user, invoice)
    except Exception as e:
        print(e)
    else:
        work.completed = True
        # work.save()
    return redirect('job:jobPage', job_id)
