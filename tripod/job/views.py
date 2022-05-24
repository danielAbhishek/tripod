import io
from datetime import datetime

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.http import FileResponse

# from job.workflow_factory.workflow import WorkFlowBase
from job.models import Job, Work, Task
from job.forms import JobReqCreateForm, JobUpdateConfirmForm, AppointmentForm

from company.models import PackageLinkProduct

from finance.models import PaymentHistory, Invoice
from finance.forms import (InvoiceUpdateForm, PaymentHistoryForm, ReceiptForm)

from tripod.utils import superuser_check, staff_check, get_company, force_password_change_check
# from tripod.tasks_lib.email import EmailClient

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


@login_required(login_url='company:staffLogin')
@user_passes_test(force_password_change_check,
                  login_url="company:changePassword")
def staffJobHomePage(request):
    """
    home page for job page, where new requests, confirmed job and declined
    job will be shown
    """
    return render(request, 'staffs/job.html')


@login_required(login_url='company:staffLogin')
@user_passes_test(staff_check, login_url='permission_error')
@user_passes_test(force_password_change_check,
                  login_url="company:changePassword")
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
@user_passes_test(force_password_change_check,
                  login_url="company:changePassword")
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
    context = {'decJobs': jobs}

    return render(request, 'jobManagement/jobDecManagement.html', context)


@login_required(login_url="company:staffLogin")
@user_passes_test(staff_check, login_url='permission_error')
@user_passes_test(force_password_change_check,
                  login_url="company:changePassword")
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
@user_passes_test(staff_check, login_url='permission_error')
@user_passes_test(force_password_change_check,
                  login_url="company:changePassword")
def jobChangeReqToJob(request, pk):
    """
    Change job request to Job
    """
    job = Job.objects.get(pk=pk)
    form = JobUpdateConfirmForm(instance=job, userObj=None, operation=None)
    context = {'form': form, 'job': job}

    if request.method == 'POST':
        form = JobUpdateConfirmForm(request.POST,
                                    instance=job,
                                    userObj=request.user,
                                    operation='confirming Job')
        if form.is_valid():
            try:
                obj = form.save()
                messages.success(request,
                                 f'Job is confirmed and updated {obj}')
                return redirect('job:jobPage', job.id)
            except ValueError as err:
                messages.error(request, err)
                return render(request, 'jobManagement/jobConfirmPage.html',
                              context)
        else:
            messages.error(request, 'Invalid form submission')

    context = {'form': form, 'job': job}
    return render(request, 'jobManagement/jobConfirmPage.html', context)


@login_required(login_url="company:staffLogin")
@user_passes_test(superuser_check, login_url="permission_error")
def delRequestJob(request, pk):
    """
    Deleting job that are in the request phase
    """
    job = Job.objects.get(pk=pk)
    context = {'job': job}
    job.delete()

    messages.success(request, f"{job} has been successfully deleted")
    return redirect('job:jobReqManagementPage')


@login_required(login_url='company:staffLogin')
@user_passes_test(staff_check, login_url='permission_error')
@user_passes_test(force_password_change_check,
                  login_url="company:changePassword")
def jobManagementPage(request):
    """
    job management page
    """
    jobs = Job.objects.filter(status='job').exclude(task_status='jbd')
    query = request.GET.get('q')
    if query is not None:
        lookup = Q(job_name__icontains=query) | Q(
            primary_client__first_name=query) | Q(
                primary_client__last_name=query)
        jobs = jobs.filter(lookup)
    context = {'jobs': jobs}

    return render(request, 'jobManagement/jobManagement.html', context)


@login_required(login_url='company:staffLogin')
@user_passes_test(staff_check, login_url='permission_error')
@user_passes_test(force_password_change_check,
                  login_url="company:changePassword")
def completedJobManagementPage(request):
    """
    job management page
    """
    jobs = Job.objects.filter(status='job').filter(task_status='jbd')
    query = request.GET.get('q')
    if query is not None:
        lookup = Q(job_name__icontains=query) | Q(
            primary_client__first_name=query) | Q(
                primary_client__last_name=query)
        jobs = jobs.filter(lookup)
    context = {'jobs': jobs}

    return render(request, 'jobManagement/completedJobManagement.html',
                  context)


@login_required(login_url="company:staffLogin")
@user_passes_test(staff_check, login_url='permission_error')
@user_passes_test(force_password_change_check,
                  login_url="company:changePassword")
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
@user_passes_test(force_password_change_check,
                  login_url="company:changePassword")
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
@user_passes_test(force_password_change_check,
                  login_url="company:changePassword")
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
@user_passes_test(force_password_change_check,
                  login_url="company:changePassword")
def processEmailTaskWithoutSendingEmail(request, pk):
    """
    processing and completing the email task from admin or business side
    without sending the email
    """
    task = Task.objects.get(pk=pk)
    work = task.work
    job = work.job

    # making sure that task is process correctly
    try:
        task.process_task(request.user, send_email=False)
        messages.success(request, f'Task {task} is successfully processed')
        return redirect('job:jobPage', job.id)
    except Exception as e:
        messages.error(request,
                       f'Exception {e} occured while processing the task')
        return redirect('job:jobPage', job.id)


@login_required(login_url='company:staffLogin')
@user_passes_test(staff_check, login_url='permission_error')
@user_passes_test(force_password_change_check,
                  login_url="company:changePassword")
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
@user_passes_test(force_password_change_check,
                  login_url="company:changePassword")
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
@user_passes_test(staff_check, login_url='permission_error')
@user_passes_test(force_password_change_check,
                  login_url="company:changePassword")
def updateInvoice(request, pk):
    """Add discount if wanted to notes before sharing invoice"""
    invoice = Invoice.objects.get(pk=pk)
    form = InvoiceUpdateForm(instance=invoice)
    job = invoice.job
    discount = invoice.discount
    invoice_completion = job.work_set.get(
        work_order=2).work_completed_percentage()

    if request.method == 'POST':
        form = InvoiceUpdateForm(request.POST, instance=invoice)
        if form.is_valid():
            if invoice_completion >= 50:
                invoice = form.save(commit=False)
                invoice.discount = discount
                invoice.save()
            else:
                invoice = form.save(commit=False)
                if invoice.discount:
                    invoice.total_price = invoice.price - (invoice.price *
                                                           invoice.discount)
                invoice.save()
            messages.success(request, f'Invoice is updated successfully')
            return redirect('company:invoiceDetail', invoice.id)
        else:
            messages.error(request, 'Invalid form submission')

    context = {
        'form': form,
        'invoice': invoice,
        'job': invoice.job,
        'invoice_completion': invoice_completion
    }
    return render(request, 'jobManagement/invoice.html', context)


@login_required(login_url='company:staffLogin')
@user_passes_test(staff_check, login_url='permission_error')
@user_passes_test(force_password_change_check,
                  login_url="company:changePassword")
def invoicePage(request, pk):
    """displaying invoice page"""
    job = Job.objects.get(pk=pk)
    invoice = job.invoice

    context = {'invoice': invoice}

    return render(request, 'jobManagement/invoicePage.html', context)


@login_required(login_url='company:staffLogin')
@user_passes_test(staff_check, login_url='permission_error')
@user_passes_test(force_password_change_check,
                  login_url="company:changePassword")
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
@user_passes_test(force_password_change_check,
                  login_url="company:changePassword")
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
@user_passes_test(force_password_change_check,
                  login_url="company:changePassword")
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


@login_required(login_url='company:staffLogin')
@user_passes_test(superuser_check, login_url='permission_error')
def declineJob(request, pk):
    """declining job"""
    job = Job.objects.get(pk=pk)
    job.status = 'dec'
    job.save()

    context = {'decJobs': Job.objects.filter(status='dec')}
    return render(request, 'jobManagement/jobDecManagement.html', context)


@login_required(login_url='company:staffLogin')
@user_passes_test(superuser_check, login_url='permission_error')
def confirmDeclinedJob(request, pk):
    """confirm back a declined job"""
    job = Job.objects.get(pk=pk)
    job.status = 'job'
    job.save()

    context = {'jobs': Job.objects.filter(status='job')}
    return render(request, 'jobManagement/jobManagement.html', context)


@login_required(login_url='company:staffLogin')
@user_passes_test(staff_check, login_url='permission_error')
@user_passes_test(force_password_change_check,
                  login_url="company:changePassword")
def downloadInvoice(request, pk):
    # creating objects for receipt
    company = get_company()
    job = Job.objects.get(pk=pk)
    pkgLink = PackageLinkProduct.objects.filter(package=job.package)
    client = job.primary_client
    invoice = job.invoice
    now = datetime.now().strftime("%d-%m-%Y")
    # creating a file-like buffer to receive PDF data
    buffer = io.BytesIO()
    # creating the PDF object, using the buffer as its file
    p = canvas.Canvas(buffer, pagesize=letter)
    p.setLineWidth(.3)

    # handling errors
    if (client.first_name is None or client.last_name is None
            or client.contact_number is None):
        messages.error(
            request,
            "Update client information correctly. Name and contact information missing"
        )
        return redirect('job:jobPage', job.id)
    elif (company.address1 is None or company.city is None
          or company.contact_number is None or company.contact_email is None):
        messages.error(
            request,
            "Update company information correctly. Address is missing")
        return redirect('job:jobPage', job.id)
    elif invoice is None:
        messages.error(request, "Please make sure invoice is ready")
        return redirect('job:jobPage', job.id)
    elif (job.package is None):
        messages.error(request, "Please make sure package is selected")
        return redirect('job:jobPage', job.id)

    # creating the pdf with items

    # ---------------------------------------------- Invoice number
    p.setFont('Helvetica', 26)
    p.drawString(30, 750, f"Invoice #{invoice.get_issue_number()}")

    # ---------------------------------------------- Header
    # company
    p.setFont('Helvetica', 15)
    p.drawString(30, 705, company.name.upper())
    p.drawString(30, 690, company.address1)
    if company.address2:
        p.drawString(30, 675, company.address2)
        p.drawString(30, 660, company.city)
        p.drawString(30, 645, company.contact_number)
        p.drawString(30, 630, company.contact_email)
    else:
        p.drawString(30, 675, company.city)
        p.drawString(30, 660, company.contact_number)
        p.drawString(30, 645, company.contact_email)
    p.drawString(500, 750, now)
    # client
    p.drawString(30, 600, client.first_name + " " + client.last_name)
    p.drawString(30, 585, client.email)
    if client.contact_number:
        p.drawString(30, 570, client.contact_number)
    # ending line
    p.line(30, 550, 580, 550)

    # ---------------------------------------------- Body
    # body header
    p.drawString(30, 535, "Billing")
    p.setFont('Helvetica', 11)
    p.drawString(30, 520, f"Selected package - {job.package}")
    p.setFont('Helvetica', 15)
    p.drawString(30, 495, "Item")
    p.drawString(300, 495, "QTY")
    p.drawString(400, 495, "Unit-price")
    p.drawString(500, 495, "Sub-total")
    p.line(30, 485, 580, 485)

    # billing table items
    x = 485
    p.setFont('Helvetica', 11)
    for item in pkgLink:
        x -= 15
        if len(item.product.product_name) > 50:
            p.drawString(30, x, item.product.product_name[:50])
            p.drawString(30, x - 15, f" -{item.product.product_name[50:]}")
            p.drawString(300, x, str(item.units))
            p.drawString(400, x, str(item.product.unit_price))
            p.drawString(500, x, str(item.price))
            x -= 15
        else:
            p.drawString(30, x, item.product.product_name)
            p.drawString(300, x, str(item.units))
            p.drawString(400, x, str(item.product.unit_price))
            p.drawString(500, x, str(item.price))

    # billing summary
    x -= 45
    p.setFont('Helvetica', 15)
    p.drawString(300, x, "Invoice Summary")
    p.line(300, x - 15, 580, x - 15)
    p.setFont('Helvetica', 11)
    p.drawString(300, x - 30, "Subtotal")
    p.drawString(500, x - 30, str(invoice.price))
    p.drawString(300, x - 45, "Discount")
    p.drawString(500, x - 45, f"{str(int(invoice.discount * 100))} %")
    p.drawString(300, x - 60, "Total")
    p.drawString(500, x - 60, str(invoice.total_price))

    # close and done
    p.showPage()
    p.save()

    # file response sets the content-disposition header so that
    # browser present the option to save the file
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='hello.pdf')
