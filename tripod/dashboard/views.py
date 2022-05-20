from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import get_user_model

from tripod.utils import superuser_check

from dashboard.dash_utils import user_kpis, company_kpis, job_kpis, invoice_kpis, paid_data, payment_graph


@login_required(login_url='company:staffLogin')
@user_passes_test(superuser_check)
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

    # invoice kpis
    df = invoice_kpis()
    invoice_kpis_data = df[df['invoice_job'].notnull()].reset_index(drop=True)

    context = {
        'client_kpis': client_kpis_data,
        'employee_kpis_data': employee_kpis_data,
        'company_kpis_data': company_kpis_data,
        'job_kpis_data': job_kpis_data,
        'invoice_kpis_data': invoice_kpis_data.to_html(classes="table table-centered table-nowrap table-hover mb-0"),
        'paid_kpi_data': paid_kpi_data,
        'payment_plot': payment_plot,
    }

    return render(request, 'dashboard/dashhome.html', context)
