from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required, user_passes_test
from django.forms.models import modelformset_factory

from core.forms import (
    AccountCreationForm,
    CustomUserChangeForm,
)
from company.models import Event, Product, Package, PackageLinkProduct
from company.forms import (
    EventForm,
    ProductForm,
    PackageForm,
    PackageLinkProductAddForm
)
from company.utils import superuser_check


def staffLoginPage(request):
    """
    Seperate view function for staffs to login, with the given
    email and password
    """
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('company:staffCompany')
    else:
        if request.method == "POST":
            email = request.POST.get('email')
            password = request.POST.get('password')

            user = authenticate(request, email=email, password=password)

            if user is None:
                messages.info(request, 'Username or password incorrect')
            elif not user.is_staff:
                messages.info(request, 'Staffs only can access')
            elif user is not None and user.is_staff:
                login(request, user)
                return redirect('company:staffCompany')
            else:
                messages.info(request, 'Username or password incorrect')

        context = {}
        return render(request, 'staffs/login.html', context)


@login_required(login_url='company:staffLogin')
def staffLogoutPage(request):
    """
    Staffs Logout view function which redirects back to
    staffs home
    """
    logout(request)
    return redirect('company:staffLogin')


@login_required(login_url='company:staffLogin')
@user_passes_test(superuser_check)
def staffCompanyHomePage(request):
    """
    Company homepage which is only visible to admin logins,
    Where the main application content will be available
    """
    return render(request, 'admin/company.html')


@login_required(login_url='company:staffLogin')
@user_passes_test(superuser_check)
def employeeManagementPage(request):
    """
    employee management page, where employee basic information will get
    rendered in the page
    """
    users = get_user_model().objects.filter(
        is_staff=True
    )
    context = {'employees': users}
    return render(
        request, 'employeeManagement/employeeManagement.html', context)


@login_required(login_url='company:staffLogin')
@user_passes_test(superuser_check)
def staffUpdatePage(request, pk):
    """
    while form showing the selected instance of the staff details
    and letting admin to edit and update the information. Also prevent
    accessing client here.
    """
    staff = get_user_model().objects.get(pk=pk)
    if staff.is_staff:
        form = CustomUserChangeForm(instance=staff)
        context = {'form': form, 'staff': staff}

        if request.method == 'POST':
            if form.is_valid():
                form.save()
            return redirect('company:employeeManagement')

        return render(request, 'employeeManagement/employee.html', context)
    else:
        username = staff.username
        messages.error(request, f'selected user {username} is not an employee')
        return render(request, '404.html')


@login_required(login_url='company:staffLogin')
@user_passes_test(superuser_check)
def staffAddPage(request):
    """
    Adding new employee
    """
    TEMP_PASS = 'temppass@12345'
    form = AccountCreationForm(password=TEMP_PASS, user_type='staff')
    if request.method == 'POST':
        form = AccountCreationForm(
            request.POST, password=TEMP_PASS, user_type='staff')
        if form.is_valid():
            try:
                user = form.save()
                messages.success(request, f'Account was created for {user}')
                return redirect('company:employeeManagement')
            except IntegrityError:
                messages.error(request, f'User cannot be created with same\
                email address - {email}')
            except Exception as e:
                messages.error(request, f'another type of error {e}')

    context = {'form': form}
    return render(request, 'employeeManagement/employeeAdd.html', context)


@login_required(login_url='company:staffLogin')
@user_passes_test(superuser_check)
def clientManagementPage(request):
    """
    client management page, where client basic information will get
    rendered in the page
    """
    clients = get_user_model().objects.filter(
        is_client=True
    )
    context = {'clients': clients}
    return render(request, 'clientManagement/clientManagement.html', context)


@login_required(login_url='company:staffLogin')
@user_passes_test(superuser_check)
def clientUpdatePage(request, pk):
    """
    while form showing the selected instance of the client details
    and letting admin to edit and update the information. Also prevent
    accessing staff here.
    """
    client = get_user_model().objects.get(pk=pk)
    if client.is_client:
        form = CustomUserChangeForm(instance=client)
        context = {'form': form, 'client': client}

        if request.method == 'POST':
            if form.is_valid():
                form.save()
            return redirect('company:clientManagement')

        return render(request, 'clientManagement/client.html', context)
    else:
        username = client.username
        messages.error(request, f'selected user {username} is not an client')
        return render(request, '404.html')


@login_required(login_url="company:staffLogin")
@user_passes_test(superuser_check)
def clientAddPage(request):
    """
    Adding new client
    """
    TEMP_PASS = 'temppass@12345'
    form = AccountCreationForm(password=TEMP_PASS, user_type='client')
    if request.method == 'POST':
        form = AccountCreationForm(
            request.POST, password=TEMP_PASS, user_type='client')
        if form.is_valid():
            try:
                client = form.save()
                messages.success(request, f'Account was created for {client}')
                return redirect('company:clientManagement')
            except IntegrityError:
                messages.error(request, f'User cannot be created with same\
                email address - {email}')
            except Exception as e:
                messages.error(request, f'another type of error {e}')
    context = {'form': form}
    return render(request, 'clientManagement/clientAdd.html', context)


@login_required(login_url="company:staffLogin")
@user_passes_test(superuser_check)
def eventManagement(request):
    """
    Showing the events where the name will be link to the detail
    page.
    """
    events = Event.objects.all()
    context = {'events': events}
    return render(request, 'packages/eventManagement.html', context)


@login_required(login_url="company:staffLogin")
@user_passes_test(superuser_check)
def eventUpdatePage(request, pk):
    """
    While checking the detail of the event also allowing the admin user
    to edit the content
    """
    event = Event.objects.get(pk=pk)
    form = EventForm(instance=event, userObj=None, operation=None)

    if request.method == "POST":
        form = EventForm(
            request.POST, instance=event,
            userObj=request.user, operation='updating')
        if form.is_valid():
            form.save()
        return redirect('company:eventManagement')

    context = {'form': form}
    return render(request, 'packages/event.html', context)


@login_required(login_url="company:staffLogin")
@user_passes_test(superuser_check)
def eventAddPage(request):
    """
    Adding a new event
    """
    form = EventForm(userObj=None, operation=None)
    if request.method == "POST":
        form = EventForm(
            request.POST, userObj=request.user, operation='creating')
        if form.is_valid():
            event = form.save()
            messages.success(request, f'Event {event} successfully created')
        return redirect('company:eventManagement')

    context = {'form': form}
    return render(request, 'packages/eventAdd.html', context)


@login_required(login_url="company:staffLogin")
@user_passes_test(superuser_check)
def productManagement(request):
    """
    Showing the products where the name will be link to the detail
    page.
    """
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'packages/productManagement.html', context)


@login_required(login_url="company:staffLogin")
@user_passes_test(superuser_check)
def productUpdatePage(request, pk):
    """
    While checking the detail of the product also allowing the admin user
    to edit the content
    """
    product = Product.objects.get(pk=pk)
    form = ProductForm(instance=product, userObj=None, operation=None)

    if request.method == "POST":
        form = ProductForm(
            request.POST, instance=product,
            userObj=request.user, operation='updating')
        if form.is_valid():
            form.save()
        return redirect('company:productManagement')
    context = {'form': form}
    return render(request, 'packages/product.html', context)


@login_required(login_url="company:staffLogin")
@user_passes_test(superuser_check)
def productAddPage(request):
    """
    Adding a new product
    """
    form = ProductForm(userObj=None, operation=None)
    if request.method == "POST":
        form = ProductForm(
            request.POST, userObj=request.user, operation='creating')
        if form.is_valid():
            product = form.save()
            messages.success(request, f'Event {product} successfully created')
        return redirect('company:productManagement')

    context = {'form': form}
    return render(request, 'packages/productAdd.html', context)


@login_required(login_url="company:staffLogin")
@user_passes_test(superuser_check)
def packageManagement(request):
    """
    Showing the products where the name will be link to the detail
    page.
    """
    packages = {'packages': []}
    packages_objs = Package.objects.all()
    for package in packages_objs:
        package_inst = {}
        product_list = []
        for product in package.products.all():
            product_list.append(product)
        package_inst['package_obj'] = package
        package_inst['product_list'] = product_list
        packages['packages'].append(package_inst)
    context = {'packages': packages}
    return render(request, 'packages/packageManagement.html', context)


@login_required(login_url="company:staffLogin")
@user_passes_test(superuser_check)
def packageUpdatePage(request, pk):
    """
    While checking the detail of the product also allowing the admin user
    to edit the content
    """
    package = Package.objects.get(pk=pk)
    packageForm = PackageForm(
        request.POST or None, instance=package,
        userObj=request.user, operation='updating')
    ProductFormSet = modelformset_factory(
        PackageLinkProduct,
        fields=('product', 'units'),
        form=PackageLinkProductAddForm, extra=0)
    product_qs = PackageLinkProduct.objects.filter(package=package)
    formset = ProductFormSet(request.POST or None, queryset=product_qs)

    if request.method == 'POST':
        if all([packageForm.is_valid(), formset.is_valid()]):
            package = packageForm.save(commit=False)
            for form in formset:
                obj, package = form.save(
                    package=package,
                    userObj=request.user, operation='updating')
            package.save()
        return redirect('company:packageManagement')

    context = {
        'packageForm': packageForm, 'formset': formset, 'package': package}
    return render(request, 'packages/package.html', context)


@login_required(login_url="company:staffLogin")
@user_passes_test(superuser_check)
def packageAddPage(request):
    """
    Adding a new product
    """
    packageForm = PackageForm(
        request.POST or None, instance=None,
        userObj=request.user, operation='creating')
    ProductFormSet = modelformset_factory(
        PackageLinkProduct,
        fields=('product', 'units'),
        form=PackageLinkProductAddForm, extra=0)
    qs = PackageLinkProduct.objects.none()
    formset = ProductFormSet(request.POST or None, queryset=qs)

    if request.method == "POST":
        if all([packageForm.is_valid(), formset.is_valid()]):
            package = packageForm.save()
            for form in formset:
                obj, package = form.save(
                    package=package,
                    userObj=request.user, operation='creating')
            package.save()
        return redirect('company:packageManagement')

    context = {'packageForm': packageForm, 'formset': formset}
    return render(request, 'packages/packageAdd.html', context)
