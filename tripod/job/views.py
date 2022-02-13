from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test

from company.utils import superuser_check


@login_required(login_url='company:staffLogin')
def staffJobHomePage(request):
    return render(request, 'staffs/job.html')
