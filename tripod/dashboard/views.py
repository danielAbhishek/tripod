import csv
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import get_user_model
from django.http import HttpResponse

from tripod.utils import staff_check, force_password_change_check

from dashboard.dash_utils import (user_kpis, company_kpis, job_kpis,
                                  invoice_kpis, paid_data, payment_graph,
                                  jobs_by_source_graph)


@login_required(login_url='company:staffLogin')
@user_passes_test(staff_check)
@user_passes_test(force_password_change_check,
                  login_url="company:changePassword")
def dashboarHome(request):
    """
    dashboard and management reports
    """
    # user management
    users = get_user_model().objects.all()
    clients = users.filter(is_client=True)
    employees = users.filter(is_staff=True)
    client_kpis_data = user_kpis(clients)
    employee_kpis_data = user_kpis(employees)

    # company kpis
    company_kpis_data = company_kpis()

    # job kpis
    job_kpis_data = job_kpis()

    # paid data
    paid_kpi_data = paid_data()

    # payment plot
    payment_plot = payment_graph()

    # source-jobs plot
    jobs_by_source = jobs_by_source_graph()

    # invoice kpis
    df = invoice_kpis()
    invoice_kpis_data = df[df['Job Name'] != 'Job Deleted'].reset_index(
        drop=True)

    context = {
        'client_kpis':
        client_kpis_data,
        'employee_kpis_data':
        employee_kpis_data,
        'company_kpis_data':
        company_kpis_data,
        'job_kpis_data':
        job_kpis_data,
        'invoice_kpis_data':
        invoice_kpis_data.to_html(
            classes="table table-centered table-nowrap table-hover mb-0"),
        'paid_kpi_data':
        paid_kpi_data,
        'payment_plot':
        payment_plot,
        'jobs_by_source_plot':
        jobs_by_source,
    }

    return render(request, 'dashboard/dashhome.html', context)


@login_required(login_url='company:staffLogin')
@user_passes_test(staff_check)
@user_passes_test(force_password_change_check,
                  login_url="company:changePassword")
def download_summary_report(request):
    """Downloading the summary invoice report into csv"""
    # Creating HttpRepsponce with csv header
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="report.csv"'},
    )

    # creating csv file
    writer = csv.writer(response)
    writer.writerow([
        "Index", "Job Name", "Job Status", "Client Email", "Package", "Event",
        "Source", "Invoice Number", "Invoice Date", "Sub Total", "Discount",
        "Net Amount", "Paid", "To be Paid", "Last Paid Date"
    ])
    for index, row in invoice_kpis().iterrows():
        writer.writerow([
            index, row['Job Name'], row['Job Status'], row['Client Email'],
            row['Package'], row['Event'], row['Source'], row['Invoice Number'],
            row['Invoice Date'], row['Sub Total'], row['Discount'],
            row['Net Amount'], row['Paid'], row['To be Paid'],
            row['Last Paid Date']
        ])
    return response
