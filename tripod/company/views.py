from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth import (authenticate, login, logout, get_user_model,
                                 update_session_auth_hash)
from django.db import IntegrityError
from django.db.models import Q
from django.db.models.deletion import RestrictedError
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.forms.models import modelformset_factory
from django.core.exceptions import ObjectDoesNotExist

from core.forms import (AccountCreationForm, CustomUserChangeForm, CompanyForm,
                        StaffProfileUpdateForm)
from core.models import Company
from company.models import (Event, Product, Package, PackageLinkProduct,
                            Equipment, EquipmentMaintanence)
from company.forms import (EventForm, ProductForm, PackageForm,
                           PackageLinkProductAddForm, EquipmentForm,
                           EquipmentMaintanenceForm)
from company.utils import superuser_check, staff_check

from finance.models import Invoice, PaymentHistory

from tripod.utils import get_company, force_password_change_check


def staffLoginPage(request):
    """
    Seperate view function for staffs to login, with the given
    email and password
    """
    if request.user.is_authenticated and request.user.is_staff:
        messages.info(request, 'Already logged in')
        return redirect('company:staffCompany')
    else:
        company = get_company()
        if request.method == "POST":
            email = request.POST.get('email')
            password = request.POST.get('password')

            user = authenticate(request, email=email, password=password)

            if user is None:
                messages.error(request, 'Username or password incorrect')
            elif not user.is_staff:
                messages.error(request, 'Staffs only can access')
            elif user is not None and user.is_staff:
                login(request, user)
                messages.success(request, 'Successfully logged in')
                return redirect('adminPage')
            else:
                messages.error(request, 'Username or password incorrect')

        context = {'company': company}
        return render(request, 'staffs/login.html', context)


@login_required(login_url='company:staffLogin')
def staffLogoutPage(request):
    """
    Staffs Logout view function which redirects back to
    staffs home
    """
    logout(request)
    messages.success(request, 'Successfully logged out')
    return redirect('company:staffLogin')


@login_required(login_url='company:staffLogin')
@user_passes_test(force_password_change_check,
                  login_url="company:changePassword")
@user_passes_test(staff_check, login_url='permission_error')
def staffCompanyHomePage(request):
    """
    Company homepage which is only visible to admin logins,
    Where the main application content will be available
    """
    company = Company.objects.filter(active=True).first()
    context = {'company': company}
    return render(request, 'admin/company.html', context)


@login_required(login_url="company:staffLogin")
@user_passes_test(staff_check, login_url='permission_error')
def changePassword(request):
    """
    Changing password of the user who logged in
    """
    form = PasswordChangeForm(request.user)
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            user.force_password_change = False
            user.password_change_code = ''
            user.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Your password was successfully updated")
            return redirect('company:staffCompany')
        else:
            messages.error(request, 'Invalid form submission')

    context = {'form': form}
    return render(request, 'staffs/change_password.html', context)


@login_required(login_url='company:staffLogin')
@user_passes_test(force_password_change_check,
                  login_url="companu:changePassword")
@user_passes_test(staff_check, login_url="permission_error")
def updateProfile(request):
    """
    user profile updating
    """
    user = request.user
    form = StaffProfileUpdateForm(instance=user)

    if request.method == "POST":
        form = StaffProfileUpdateForm(request.POST or None, instance=user)

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
            user.save()
            messages.success(request, "Successfully update the profile")
            return redirect('company:staffCompany')
        else:
            messages.error(request, "Invalid form submission")
            return render(request, 'staffs/update_profile.html', context)

    context = {"form": form}
    return render(request, 'staffs/update_profile.html', context)


@login_required(login_url='company:staffLogin')
@user_passes_test(superuser_check, login_url="permission_error")
def employeeManagementPage(request):
    """
    employee management page, where employee basic information will get
    rendered in the page
    """
    query = request.GET.get('q')
    users = get_user_model().objects.filter(is_staff=True)
    if query is not None:
        lookup = Q(email__icontains=query) | Q(
            first_name__icontains=query) | Q(last_name__icontains=query)
        users = users.filter(lookup)

    context = {'employees': users}
    return render(request, 'employeeManagement/employeeManagement.html',
                  context)


@login_required(login_url='company:staffLogin')
@user_passes_test(superuser_check, login_url="permission_error")
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
            form = CustomUserChangeForm(request.POST or None, instance=staff)
            if form.is_valid():
                staff.email = form.cleaned_data['email']
                staff.username = form.cleaned_data['username']
                staff.first_name = form.cleaned_data['first_name']
                staff.last_name = form.cleaned_data['last_name']
                staff.gender = form.cleaned_data['gender']
                staff.contact_number = form.cleaned_data['contact_number']
                staff.contact_number_2 = form.cleaned_data['contact_number_2']
                staff.address = form.cleaned_data['address']
                staff.address_2 = form.cleaned_data['address_2']
                staff.city = form.cleaned_data['city']
                staff.province = form.cleaned_data['province']
                staff.country = form.cleaned_data['country']
                staff.is_client = False
                staff.is_staff = True
                staff.is_active = form.cleaned_data['is_active']
                staff.is_superuser = form.cleaned_data['is_superuser']
                staff.save()
                if staff.is_active:
                    messages.success(
                        request, f'Successfully updated records for {staff}')
                    return redirect('company:employeeManagement')
                else:
                    messages.success(request, f'Deactivated {staff}')
                    return redirect('company:employeeManagement')
            else:
                messages.error(request, 'Form is entered with invalid records')
                return render(request, 'employeeManagement/employee.html',
                              context)

        return render(request, 'employeeManagement/employee.html', context)
    else:
        username = staff.username
        messages.error(request, f'selected user {username} is not an employee')
        return render(request, '404.html')


@login_required(login_url='company:staffLogin')
@user_passes_test(superuser_check, login_url="permission_error")
def staffAddPage(request):
    """
    Adding new employee
    """
    context = {}
    form = AccountCreationForm(user_type='staff')
    if request.method == 'POST':
        form = AccountCreationForm(request.POST, user_type='staff')
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Account was created for {user}')
            return redirect('company:employeeManagement')
        else:
            messages.error(request, 'Invalid form submission')

    context = {'form': form}
    return render(request, 'employeeManagement/employeeAdd.html', context)


@login_required(login_url='company:staffLogin')
@user_passes_test(superuser_check, login_url="permission_error")
def clientManagementPage(request):
    """
    client management page, where client basic information will get
    rendered in the page
    """
    query = request.GET.get('q')
    clients = get_user_model().objects.filter(is_client=True)
    if query is not None:
        lookup = Q(email__icontains=query) | Q(
            first_name__icontains=query) | Q(last_name__icontains=query)
        clients = clients.filter(lookup)
    context = {'clients': clients}
    return render(request, 'clientManagement/clientManagement.html', context)


@login_required(login_url='company:staffLogin')
@user_passes_test(superuser_check, login_url="permission_error")
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
            form = CustomUserChangeForm(request.POST, instance=client)
            if form.is_valid():
                client.email = form.cleaned_data['email']
                client.username = form.cleaned_data['username']
                client.first_name = form.cleaned_data['first_name']
                client.last_name = form.cleaned_data['last_name']
                client.gender = form.cleaned_data['gender']
                client.contact_number = form.cleaned_data['contact_number']
                client.contact_number_2 = form.cleaned_data['contact_number_2']
                client.address = form.cleaned_data['address']
                client.address_2 = form.cleaned_data['address_2']
                client.city = form.cleaned_data['city']
                client.province = form.cleaned_data['province']
                client.country = form.cleaned_data['country']
                client.is_staff = False
                client.is_client = True
                client.is_superuser = False
                client.is_active = form.cleaned_data['is_active']
                client.save()
                if client.is_active:
                    messages.success(
                        request, f'Successfully updated records for {client}')
                    return redirect('company:clientManagement')
                else:
                    messages.success(request, f'Deactivated {client}')
                    return redirect('company:clientManagement')
            else:
                messages.error(request, 'Form is entered with invalid records')
                return render(request, 'clientManagement/client.html', context)

        return render(request, 'clientManagement/client.html', context)
    else:
        username = client.username
        messages.error(request, f'selected user {username} is not an client')
        return render(request, '404.html')


@login_required(login_url="company:staffLogin")
@user_passes_test(superuser_check, login_url='permission_error')
def userDeletePage(request, pk):
    """
    Delete a client profile
    """
    user = get_user_model().objects.get(pk=pk)
    user_email = user.email
    user_type = user.is_staff
    try:
        user.delete()
        messages.success(request, f"{user_email} has been successfully deleted")
    except RestrictedError:
        messages.error(request, f"Cannot delete {user_email} has links with Job and other parts! delete job first")

    if user_type:
        return redirect('company:employeeManagement')
    else:
        return redirect('company:clientManagement')


@login_required(login_url="company:staffLogin")
@user_passes_test(superuser_check, login_url="permission_error")
def clientAddPage(request):
    """
    Adding new client
    """
    form = AccountCreationForm(user_type='client')
    if request.method == 'POST':
        form = AccountCreationForm(request.POST, user_type='client')
        if form.is_valid():
            client = form.save()
            messages.success(request, f'Account was created for {client}')
            return redirect('company:clientManagement')
        else:
            messages.error(request, 'Invalid form submission')

    context = {'form': form}
    return render(request, 'clientManagement/clientAdd.html', context)


@login_required(login_url="company:staffLogin")
@user_passes_test(force_password_change_check,
                  login_url="companu:changePassword")
@user_passes_test(staff_check, login_url='permission_error')
def eventManagement(request):
    """
    Showing the events where the name will be link to the detail
    page.
    """
    query = request.GET.get('q')
    events = None
    if query is not None:
        lookup = Q(event_name__icontains=query)
        events = Event.objects.filter(lookup)
    else:
        events = Event.objects.all()
    context = {'events': events}
    return render(request, 'packages/eventManagement.html', context)


@login_required(login_url="company:staffLogin")
@user_passes_test(force_password_change_check,
                  login_url="companu:changePassword")
@user_passes_test(staff_check, login_url='permission_error')
def eventUpdatePage(request, pk):
    """
    While checking the detail of the event also allowing the admin user
    to edit the content
    """
    event = Event.objects.get(pk=pk)
    form = EventForm(instance=event, userObj=None, operation=None)

    if request.method == "POST":
        form = EventForm(request.POST,
                         instance=event,
                         userObj=request.user,
                         operation='updating')
        if form.is_valid():
            event = form.save()
            messages.success(request, f'Event {event} successfully updated')
            return redirect('company:eventManagement')
        else:
            messages.error(request, 'Invalid form submission')

    context = {'form': form, 'event': event}
    return render(request, 'packages/event.html', context)


@login_required(login_url="company:staffLogin")
@user_passes_test(force_password_change_check,
                  login_url="companu:changePassword")
@user_passes_test(staff_check, login_url='permission_error')
def eventAddPage(request):
    """
    Adding a new event
    """
    form = EventForm(userObj=None, operation=None)
    if request.method == "POST":
        form = EventForm(request.POST,
                         userObj=request.user,
                         operation='creating')
        if form.is_valid():
            event = form.save()
            messages.success(request, f'Event {event} successfully created')
            return redirect('company:eventManagement')
        else:
            messages.error(request, 'Invalid form submission')

    context = {'form': form}
    return render(request, 'packages/eventAdd.html', context)


@login_required(login_url="company:staffLogin")
@user_passes_test(superuser_check, login_url='permission_error')
def eventDeletePage(request, pk):
    """
    Delete an event
    """
    event = Event.objects.get(pk=pk)
    event_name = event.event_name
    event.delete()

    messages.success(request, f"{event_name} has been successfully deleted")
    return redirect('company:eventManagement')


@login_required(login_url="company:staffLogin")
@user_passes_test(force_password_change_check,
                  login_url="companu:changePassword")
@user_passes_test(staff_check, login_url='permission_error')
def productManagement(request):
    """
    Showing the products where the name will be link to the detail
    page.
    """
    query = request.GET.get('q')
    products = None
    if query is not None:
        lookup = Q(product_name__icontains=query)
        products = Product.objects.filter(lookup)
    else:
        products = Product.objects.all()
    context = {'products': products}
    return render(request, 'packages/productManagement.html', context)


@login_required(login_url="company:staffLogin")
@user_passes_test(force_password_change_check,
                  login_url="companu:changePassword")
@user_passes_test(staff_check, login_url='permission_error')
def productUpdatePage(request, pk):
    """
    While checking the detail of the product also allowing the admin user
    to edit the content
    """
    product = Product.objects.get(pk=pk)
    form = ProductForm(instance=product, userObj=None, operation=None)

    if request.method == "POST":
        form = ProductForm(request.POST,
                           instance=product,
                           userObj=request.user,
                           operation='updating')
        if form.is_valid():
            product = form.save()
            messages.success(request,
                             f'Product {product} successfully updated')
            return redirect('company:productManagement')
        else:
            messages.error(request, 'Invalid form submission')

    context = {'form': form, 'product': product}
    return render(request, 'packages/product.html', context)


@login_required(login_url="company:staffLogin")
@user_passes_test(superuser_check, login_url='permission_error')
def productDeletePage(request, pk):
    """
    Delete an product
    """
    product = Product.objects.get(pk=pk)
    product_name = product.product_name
    product.delete()

    messages.success(request, f"{product_name} has been successfully deleted")
    return redirect('company:productManagement')


@login_required(login_url="company:staffLogin")
@user_passes_test(force_password_change_check,
                  login_url="companu:changePassword")
@user_passes_test(staff_check, login_url='permission_error')
def productAddPage(request):
    """
    Adding a new product
    """
    form = ProductForm(userObj=None, operation=None)
    if request.method == "POST":
        form = ProductForm(request.POST,
                           userObj=request.user,
                           operation='creating')
        if form.is_valid():
            product = form.save()
            messages.success(request,
                             f'Product {product} successfully created')
            return redirect('company:productManagement')
        else:
            messages.error(request, 'Invalid form submission')

    context = {'form': form}
    return render(request, 'packages/productAdd.html', context)


@login_required(login_url="company:staffLogin")
@user_passes_test(force_password_change_check,
                  login_url="companu:changePassword")
@user_passes_test(staff_check, login_url='permission_error')
def packageManagement(request):
    """
    Showing the products where the name will be link to the detail
    page.
    """
    query = request.GET.get('q')
    packages_objs = None
    if query is not None:
        lookup = Q(package_name__icontains=query)
        packages_objs = Package.objects.filter(lookup)
    else:
        packages_objs = Package.objects.all().order_by('-changed_at')
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
    return render(request, 'packages/packageManagement.html', context)


@login_required(login_url="company:staffLogin")
@user_passes_test(force_password_change_check,
                  login_url="companu:changePassword")
@user_passes_test(staff_check, login_url='permission_error')
def packageUpdatePage(request, pk):
    """
    While checking the detail of the product also allowing the admin user
    to edit the content
    """
    package = Package.objects.get(pk=pk)
    packageForm = PackageForm(request.POST or None,
                              instance=package,
                              userObj=request.user,
                              operation='updating')
    ProductFormSet = modelformset_factory(PackageLinkProduct,
                                          fields=('product', 'units'),
                                          form=PackageLinkProductAddForm,
                                          extra=0)
    product_qs = PackageLinkProduct.objects.filter(package=package)
    formset = ProductFormSet(request.POST or None, queryset=product_qs)

    if request.method == 'POST':
        if all([packageForm.is_valid(), formset.is_valid()]):
            package = packageForm.save(commit=False)
            for form in formset:
                obj, package = form.save(package=package,
                                         userObj=request.user,
                                         operation='updating')
            print(package.is_active)
            package.save()
            messages.success(request,
                             f'Package {package} successfully updated')
            return redirect('company:packageManagement')
        else:
            messages.error(request, 'Invalid form submission')

    context = {
        'packageForm': packageForm,
        'formset': formset,
        'package': package
    }
    return render(request, 'packages/package.html', context)


@login_required(login_url="company:staffLogin")
@user_passes_test(force_password_change_check,
                  login_url="companu:changePassword")
@user_passes_test(staff_check, login_url='permission_error')
def packageAddPage(request):
    """
    Adding a new product
    """
    packageForm = PackageForm(request.POST or None,
                              instance=None,
                              userObj=request.user,
                              operation='creating')
    ProductFormSet = modelformset_factory(PackageLinkProduct,
                                          fields=('product', 'units'),
                                          form=PackageLinkProductAddForm,
                                          extra=0)
    qs = PackageLinkProduct.objects.none()
    formset = ProductFormSet(request.POST or None, queryset=qs)

    if request.method == "POST":
        if all([packageForm.is_valid(), formset.is_valid()]):
            package = packageForm.save()
            for form in formset:
                obj, package = form.save(package=package,
                                         userObj=request.user,
                                         operation='creating')
            package.save()
            messages.success(request,
                             f'Package {package} successfully created')
            return redirect('company:packageManagement')
        else:
            messages.error(request, 'Invalid form submission')

    context = {'packageForm': packageForm, 'formset': formset}
    return render(request, 'packages/packageAdd.html', context)


@login_required(login_url="company:staffLogin")
@user_passes_test(superuser_check, login_url='permission_error')
def invoiceManagement(request):
    """
    Showing the invoice where the name will be link to the detail
    page.
    """
    query = request.GET.get('q')
    invoices = None
    if query is not None:
        lookup = Q(job__job_name__icontains=query)
        invoices = Invoice.objects.filter(lookup)
    else:
        invoices = Invoice.objects.all()
    context = {'invoices': invoices}
    return render(request, 'finance/invoice.html', context)


@login_required(login_url="company:staffLogin")
@user_passes_test(superuser_check, login_url='permission_error')
def invoiceDeletePage(request, pk):
    """
    Delete an invoice
    """
    invoice = Invoice.objects.get(pk=pk)
    invoice_id = invoice.get_issue_number()
    invoice.delete()

    messages.success(request, f"Invoice {invoice_id} has been successfully deleted")
    return redirect('company:invoiceManagement')


@login_required(login_url="company:staffLogin")
@user_passes_test(superuser_check, login_url='permission_error')
def invoiceDetail(request, pk):
    """
    Showing the products where the name will be link to the detail
    page.
    """
    invoice = Invoice.objects.get(pk=pk)
    try:
        job = invoice.job
        pkgLink = PackageLinkProduct.objects.filter(package=job.package)
    except ObjectDoesNotExist:
        invoice.job = None
        pkgLink = None
    company = get_company()
    context = {'invoice': invoice, 'pkgLink': pkgLink, 'company': company}
    return render(request, 'finance/invoiceDetail.html', context)


@login_required(login_url="company:staffLogin")
@user_passes_test(force_password_change_check,
                  login_url="companu:changePassword")
@user_passes_test(staff_check, login_url='permission_error')
def equipmentManagement(request):
    """
    Showing the equipments where the name will be link to the detail
    page.
    """
    query = request.GET.get('q')
    equipments = None
    if query is not None:
        lookup = Q(equipment_name__icontains=query)
        equipments = Equipment.objects.filter(lookup)
    else:
        equipments = Equipment.objects.all()
    context = {'equipments': equipments}
    return render(request, 'equipment/equipmentManagement.html', context)


@login_required(login_url="company:staffLogin")
@user_passes_test(force_password_change_check,
                  login_url="companu:changePassword")
@user_passes_test(staff_check, login_url='permission_error')
def equipmentUpdatePage(request, pk):
    """
    While checking the detail of the equipment also allowing the admin user
    to edit the content
    """
    equipment = Equipment.objects.get(pk=pk)
    form = EquipmentForm(instance=equipment)

    if request.method == "POST":
        form = EquipmentForm(request.POST, instance=equipment)
        if form.is_valid():
            equip = form.save()
            messages.success(request,
                             f'Equipment {equip} successfully updated')
            return redirect('company:equipmentManagement')
        else:
            messages.error(request, 'Invalid form submission')

    context = {'form': form, 'equipment': equipment}
    return render(request, 'equipment/equipment.html', context)


@login_required(login_url="company:staffLogin")
@user_passes_test(superuser_check, login_url='permission_error')
def equipmentDeletePage(request, pk):
    """
    Delete an equipment
    """
    equipment = Equipment.objects.get(pk=pk)
    equipment_name = equipment.equipment_name
    equipment.delete()

    messages.success(request, f"{equipment_name} has been successfully deleted")
    return redirect('company:equipmentManagement')


@login_required(login_url="company:staffLogin")
@user_passes_test(force_password_change_check,
                  login_url="companu:changePassword")
@user_passes_test(staff_check, login_url='permission_error')
def equipmentAddPage(request):
    """
    Adding a new event
    """
    form = EquipmentForm()
    if request.method == "POST":
        form = EquipmentForm(request.POST)
        if form.is_valid():
            equipment = form.save()
            messages.success(request,
                             f'Equipment {equipment} successfully created')
            return redirect('company:equipmentManagement')
        else:
            messages.error(request, 'Invalid form submission')

    context = {'form': form}
    return render(request, 'equipment/equipmentAdd.html', context)


@login_required(login_url="company:staffLogin")
@user_passes_test(force_password_change_check,
                  login_url="companu:changePassword")
@user_passes_test(staff_check, login_url='permission_error')
def equipmentMaintanence(request):
    """
    Showing the equipments maintanence page
    """
    query = request.GET.get('q')
    equipments = None
    if query is not None:
        lookup = Q(equipment__equipment_name__icontains=query)
        equipments = EquipmentMaintanence.objects.filter(lookup)
    else:
        equipments = EquipmentMaintanence.objects.all()
    context = {'equipments': equipments}
    return render(request, 'equipment/equipmentsMaintanence.html', context)


@login_required(login_url="company:staffLogin")
@user_passes_test(force_password_change_check,
                  login_url="companu:changePassword")
@user_passes_test(staff_check, login_url='permission_error')
def equipmentMaintanenceUpdatePage(request, pk):
    """
    While checking the detail of the equipment Maintanence also allowing the admin user
    to edit the content
    """
    equipment = EquipmentMaintanence.objects.get(pk=pk)
    form = EquipmentMaintanenceForm(instance=equipment)

    if request.method == "POST":
        form = EquipmentMaintanenceForm(request.POST, instance=equipment)
        if form.is_valid():
            obj = form.save()
            messages.success(
                request, f'Equipment Maintanence {obj} successfully updated')
            return redirect('company:equipmentMaintanence')
        else:
            messages.error(request, 'Invalid form submission')

    context = {'form': form, 'equipment': equipment}
    return render(request, 'equipment/equipmentMaintanence.html', context)


@login_required(login_url="company:staffLogin")
@user_passes_test(superuser_check, login_url='permission_error')
def equipmentMaintanenceDeletePage(request, pk):
    """
    Delete an equipmentMaintanence
    """
    equipmentMaintanence = EquipmentMaintanence.objects.get(pk=pk)
    equipmentMaintanence_name = equipmentMaintanence.equipment
    equipmentMaintanence.delete()

    messages.success(request, f"{equipmentMaintanence_name} has been successfully deleted")
    return redirect('company:equipmentMaintanence')


@login_required(login_url="company:staffLogin")
@user_passes_test(force_password_change_check,
                  login_url="companu:changePassword")
@user_passes_test(staff_check, login_url='permission_error')
def equipmentMaintanenceAddPage(request):
    """
    Adding a new equipment maintanence
    """
    form = EquipmentMaintanenceForm()
    if request.method == "POST":
        form = EquipmentMaintanenceForm(request.POST)
        if form.is_valid():
            equipment = form.save()
            messages.success(
                request,
                f'Equipment Maintanence ({equipment}) successfully created')
            return redirect('company:equipmentMaintanence')
        else:
            messages.error(request, 'Invalid form submission')

    context = {'form': form}
    return render(request, 'equipment/equipmentMaintanenceAdd.html', context)


@login_required(login_url="company:staffLogin")
@user_passes_test(force_password_change_check,
                  login_url="companu:changePassword")
@user_passes_test(staff_check, login_url='permission_error')
def companyUpdate(request, pk):
    company = Company.objects.get(pk=pk)
    form = CompanyForm(instance=company)
    if request.method == "POST":
        form = CompanyForm(request.POST, instance=company)
        if form.is_valid():
            company = form.save(commit=False)
            company.active = True
            company.save()
            messages.success(request, f'Company {company} successfully added')
            return redirect('company:staffCompany')
        else:
            messages.error(request, 'Invalid form submission')

    context = {'form': form, 'company': company}
    return render(request, 'admin/companyUpdate.html', context)
