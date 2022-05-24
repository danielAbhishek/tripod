from datetime import datetime, timedelta
from django.db.models import Q
from django.db.models import Avg, Count, Min, Sum
from django.core.exceptions import ObjectDoesNotExist

from company.models import (Event, Product, Package, Equipment,
                            EquipmentMaintanence, PackageLinkProduct)

from job.models import Job

from finance.models import Invoice, PaymentHistory

from settings.models import Source

import pandas as pd
import matplotlib.pyplot as plt
import base64
from io import BytesIO


def user_kpis(obj):
    """
    user KPIs
    """
    total_users = len(obj)
    total_active_users = len(obj.filter(is_active=True))
    """Preparing joined bucket"""
    # getting dates that were before 10, 20, 30 days
    date_thirty_days_before = datetime.now().date() - timedelta(days=30)
    date_ten_days_before = datetime.now().date() - timedelta(days=10)

    lookup_thirty_above = Q(date_joined__gte=date_thirty_days_before)
    lookup_ten_to_thirty = Q(date_joined__gte=date_ten_days_before) & Q(
        date_joined__lte=date_thirty_days_before)
    lookup_below_ten = Q(date_joined__lte=date_ten_days_before)

    joined_thirty_plus_users = len(obj.filter(lookup_thirty_above))
    joined_ten_to_thirty_users = len(obj.filter(lookup_ten_to_thirty))
    joined_below_ten_users = len(obj.filter(lookup_below_ten))

    data = {
        'total_users': total_users,
        'total_active_users': total_active_users,
        'joined_thirty_plus_users': joined_thirty_plus_users,
        'joined_ten_to_thirty_users': joined_ten_to_thirty_users,
        'joined_below_ten_users': joined_below_ten_users
    }

    return data


def company_kpis():
    events = len(Event.objects.all())
    products = len(Product.objects.all())
    active_products = len(Product.objects.filter(is_active=True))
    equipments = len(Equipment.objects.all())
    equip_by_availability = Equipment.objects.values('availability').annotate(
        equipments=Count('id'))
    packages = len(Package.objects.all())
    count_of_products_by_packages = PackageLinkProduct.objects.values(
        'package').annotate(products=Count('product'), price=Sum('price'))

    job_by_package = Job.objects.values('package__package_name').annotate(
        jobs_count=Count('id')).order_by('-jobs_count')

    data = {
        'total_events': events,
        'total_products': products,
        'active_products': active_products,
        'total_equipments': equipments,
        'equip_by_availability': equip_by_availability,
        'total_packages': packages,
        'job_by_package': job_by_package[:3],
        'count_of_products_by_packages': count_of_products_by_packages
    }

    return data


def job_kpis():
    jobs_task_data = {}

    job_by_sources = Job.objects.values('source').annotate(jobs=Count('id'))
    job_by_events = Job.objects.values('event__event_name').annotate(
        jobs=Count('id'))
    job_by_package = Job.objects.values('package__package_name').annotate(
        jobs=Count('id'))
    job_by_clients = Job.objects.values('primary_client__email').annotate(
        jobs=Count('id'))

    # getting tasks info
    jobs = Job.objects.all()
    for job in jobs:
        # total number of tasks
        total_tasks = len(job.get_tasks())

        # completed tasks
        completed_task_lookup = Q(completed=True)
        completed_tasks = len(job.get_tasks(lookup=completed_task_lookup))

        # user tasks
        user_task_lookup = Q(user_task=True)
        user_tasks = len(job.get_tasks(lookup=user_task_lookup))

        # user inputs needed tasks
        user_input_need_task_lookup = Q(user_completed='su')
        user_pending_task = len(
            job.get_tasks(lookup=user_input_need_task_lookup))

        # user completed tasks
        user_completed_task_lookup = Q(user_completed='uc') & Q(
            completed=False)
        user_completed_task = len(
            job.get_tasks(lookup=user_completed_task_lookup))

        # invoice and contract pending task_set
        invoice_pending_lookup = Q(task_type='cn') & Q(user_completed='su')
        invoice_pending_task = len(
            job.get_tasks(lookup=invoice_pending_lookup))

        # appointment pending task_set
        app_pending_lookup = Q(task_type='ap') & Q(user_completed='su')
        app_pending_task = len(job.get_tasks(lookup=app_pending_lookup))

        # questionnaire pending task_set
        quest_pending_lookup = Q(task_type='qn') & Q(user_completed='su')
        quest_pending_task = len(job.get_tasks(lookup=quest_pending_lookup))

        task_data = {
            'total_tasks': total_tasks,
            'completed_tasks': completed_tasks,
            'user_tasks': user_tasks,
            'user_pending_task': user_pending_task,
            'user_completed_task': user_completed_task,
            'invoice_pending_task': invoice_pending_task,
            'app_pending_task': app_pending_task,
            'quest_pending_task': quest_pending_task
        }
        jobs_task_data[job] = task_data

    data = {
        'jobs_task_data': jobs_task_data,
        'job_by_sources': job_by_sources,
        'job_by_events': job_by_events,
        'job_by_package': job_by_package,
        'job_by_clients': job_by_clients
    }
    return data


def invoice_kpis():
    invoice_data = {
        'Job Name': [],
        'Job Status': [],
        'Client Email': [],
        'Package': [],
        'Event': [],
        'Source': [],
        'Invoice Number': [],
        'Invoice Date': [],
        'Sub Total': [],
        'Discount': [],
        'Net Amount': [],
        'Paid': [],
        'To be Paid': [],
        'Last Paid Date': []
    }

    invoices = Invoice.objects.all()
    for invoice in invoices:
        invoice_job = None
        try:
            if invoice.job:
                invoice_job = invoice.job
                invoice_job_status = invoice.job.get_detail_task_status()
                user = invoice.job.primary_client
                package = invoice.job.package
                event = invoice.job.event
                source = invoice.job.source
        except ObjectDoesNotExist:
            invoice_job = 'Job Deleted'
            invoice_job_status = 'No Status'
            user = 'No User'
            package = 'No Package'
            event = 'No Event'
            source = 'No Source'

        invoice_data['Job Name'].append(invoice_job)
        invoice_data['Job Status'].append(invoice_job_status)
        invoice_data['Client Email'].append(user)
        invoice_data['Package'].append(package)
        invoice_data['Event'].append(event)
        invoice_data['Source'].append(source)
        invoice_data['Invoice Number'].append(invoice.get_issue_number())
        invoice_data['Invoice Date'].append(invoice.issue_date.date())
        invoice_data['Sub Total'].append(invoice.price)
        invoice_data['Discount'].append(
            str(int(invoice.discount * 100)) + " %")
        invoice_data['Net Amount'].append(invoice.total_price)
        invoice_data['Paid'].append(invoice.paid())
        invoice_data['To be Paid'].append(invoice.to_be_paid())
        invoice_data['Last Paid Date'].append(invoice.last_paid_date())

    df = pd.DataFrame(data=invoice_data)
    return df


def paid_data():
    seven_days_before = datetime.now().date() - timedelta(days=7)
    thirty_days_before = datetime.now().date() - timedelta(days=30)

    last_seven_days_deposits = PaymentHistory.objects.filter(
        payment_date__gte=seven_days_before).annotate(
            deposits=Sum('payment_amount')).last()
    last_thirty_days_deposits = PaymentHistory.objects.filter(
        payment_date__gte=thirty_days_before).annotate(
            deposits=Sum('payment_amount')).last()

    data = {
        'last_seven_days_deposits': last_seven_days_deposits,
        'last_thirty_days_deposits': last_thirty_days_deposits
    }

    return data


def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph


def get_plot(x, y, data, plt_type="line"):
    plt.switch_backend('AGG')
    plt.figure(figsize=(8, 4))
    # plt.title('Payment History')
    if plt_type == "line":
        plt.plot(x, y)
    else:
        plt.bar(x, y)
    plt.xticks(rotation=45)
    plt.xlabel(data['xlabel'])
    plt.ylabel(data['ylabel'])
    plt.tight_layout()
    graph = get_graph()
    return graph


def payment_graph():
    qs = PaymentHistory.objects.values('payment_date').annotate(
        payment_amount=Sum('payment_amount')).order_by('payment_date')
    x = [x['payment_date'].strftime("%Y-%m-%d") for x in qs]
    y = [x['payment_amount'] for x in qs]
    data = {'xlabel': 'Payment Date', 'ylabel': 'Payment'}
    chart = get_plot(x, y, data)
    return chart


def jobs_by_source_graph():
    qs = Job.objects.values('source').annotate(
        jobs=Count('id')).order_by('source')
    x = []
    y = []
    for item in qs:
        if item['source'] is None:
            x.append('No Source')
        else:
            x.append(Source.objects.get(pk=item['source']).source)
        y.append(item['jobs'])

    #  x = [Source.objects.get(pk=x['source']).source for x in qs if x is not None else "NIL"]
    #  y = [y['jobs'] for y in qs]
    data = {'xlabel': 'Sources', 'ylabel': 'Jobs'}
    chart = get_plot(x, y, data, plt_type="bar")
    return chart
