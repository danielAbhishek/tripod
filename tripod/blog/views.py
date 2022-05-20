from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages

from blog.forms import CustomerCreationForm
from company.models import Package


def tripodPage(request):
    """
    Account registration view function for customers or users
    using email, username and password
    """
    context = {}
    return render(request, 'main/tripodPage.html', context)


def contactPage(request):
    """
    Account registration view function for customers or users
    using email, username and password
    """
    # if request.user.is_authenticated:
    #     return redirect('core:home')
    # else:
    form = CustomerCreationForm()
    if request.method == "POST":
        form = CustomerCreationForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('email')
            messages.success(request, f'Account was created for {user}')
            return redirect('core:login')
        else:
            messages.error(request, 'Invalid form submission')

    context = {'reg_form': form}
    return render(request, 'main/contactUs.html', context)


def featuresPage(request):
    """
    a features page, where all the packages details will be shown 
    and additional information will be provided
    """
    packages_objs = Package.objects.all()
    packages = {'packages': []}
    for package in packages_objs:
        package_inst = {}
        product_list = []
        for product in package.products.all():
            product_list.append(product)
        package_inst['package_obj'] = package
        package_inst['product_list'] = product_list
        packages['packages'].append(package_inst)
    context = {'packages': packages}

    return render(request, 'main/features.html', context)
