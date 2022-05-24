from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import redirect, render
from django.contrib import messages

from settings.models import (Workflow, EmailTemplate, ContractTemplate,
                             QuestionnaireTemplate, Source, WorkTemplate)
from settings.forms import (WorkflowForm, WorkTemplateForm, EmailTemplateForm,
                            ContractTemplateForm, QuestionnaireTemplateForm)

from tripod.utils import superuser_check


@login_required(login_url='company:staffLogin')
@user_passes_test(superuser_check, login_url="permission_error")
def staffSettingsPage(request):
    """
    Settings homepage which is only visible to admin logins,
    Where the main application content will be available
    """
    return render(request, 'admin/settings.html')


@login_required(login_url='company:staffLogin')
@user_passes_test(superuser_check, login_url="permission_error")
def workflowManagement(request):
    """
    workflow management page, where you can define the workflow
    which will be linked to workflow automation for job creation
    """
    workflows = Workflow.objects.all()
    context = {'workflows': workflows}

    return render(request, 'workflowManagement/workflowManagement.html',
                  context)


@login_required(login_url='company:staffLogin')
@user_passes_test(superuser_check, login_url="permission_error")
def workflowUpdatePage(request, pk):
    """
    updating the workflow item
    """
    workflow = Workflow.objects.get(pk=pk)
    form = WorkflowForm(instance=workflow, userObj=None, operation=None)

    if request.method == "POST":
        form = WorkflowForm(request.POST,
                            instance=workflow,
                            userObj=request.user,
                            operation='updating')
        if form.is_valid():
            obj = form.save()
            messages.success(request, f'Workflow {obj} successfully updated')
            return redirect('settings:workflowManagement')
        else:
            messages.error(request, 'Invalid form submission')

    context = {'form': form, 'workflow': workflow}
    return render(request, 'workflowManagement/workflow.html', context)


@login_required(login_url='company:staffLogin')
@user_passes_test(superuser_check, login_url="permission_error")
def workflowAddPage(request):
    """
    Adding new workflow
    """
    form = WorkflowForm(userObj=None, operation=None)
    if request.method == "POST":
        form = WorkflowForm(request.POST,
                            userObj=request.user,
                            operation='creating')
        if form.is_valid():
            obj = form.save()
            messages.success(request, f'Workflow {obj} successfully added')
            return redirect('settings:workflowManagement')
        else:
            messages.error(request, 'Invalid form submission')

    context = {'form': form}
    return render(request, 'workflowManagement/workflowAdd.html', context)


@login_required(login_url='company:staffLogin')
@user_passes_test(superuser_check, login_url="permission_error")
def workTemplateManagement(request):
    """
    work Template management page, where you can define the work template
    that is responsible for work creation
    """
    workTemplates = WorkTemplate.objects.all()
    context = {'workTemplates': workTemplates}

    return render(request, 'workflowManagement/workTemplateManagement.html',
                  context)


@login_required(login_url='company:staffLogin')
@user_passes_test(superuser_check, login_url="permission_error")
def workTemplateUpdatePage(request, pk):
    """
    updating the work template
    """
    work_template = WorkTemplate.objects.get(pk=pk)
    form = WorkTemplateForm(instance=work_template)

    if request.method == "POST":
        form = WorkTemplateForm(request.POST, instance=work_template)
        if form.is_valid():
            obj = form.save()
            messages.success(request,
                             f'Work Template {obj} successfully updated')
            return redirect('settings:workTemplateManagement')
        else:
            messages.error(request, 'Invalid form submission')

    context = {'form': form, 'workTemplate': work_template}
    return render(request, 'workflowManagement/workTemplate.html', context)


@login_required(login_url='company:staffLogin')
@user_passes_test(superuser_check, login_url="permission_error")
def workTemplateAddPage(request):
    """
    Adding new work template
    """
    form = WorkTemplateForm()
    if request.method == "POST":
        form = WorkTemplateForm(request.POST)
        if form.is_valid():
            obj = form.save()
            messages.success(request, f'Workflow {obj} successfully added')
            return redirect('settings:workTemplateManagement')
        else:
            messages.error(request, 'Invalid form submission')

    context = {'form': form}
    return render(request, 'workflowManagement/workTemplateAdd.html', context)


@login_required(login_url='company:staffLogin')
@user_passes_test(superuser_check, login_url="permission_error")
def emailTemplateManagement(request):
    """
    email Template management page, where you can define the email template
    that is responsible for email template creation
    """
    emailTemplates = EmailTemplate.objects.all()
    context = {'emailTemplates': emailTemplates}

    return render(request, 'templateManagement/emailTemplateManagement.html',
                  context)


@login_required(login_url='company:staffLogin')
@user_passes_test(superuser_check, login_url="permission_error")
def emailTemplateUpdatePage(request, pk):
    """
    updating the email template
    """
    email_template = EmailTemplate.objects.get(pk=pk)
    form = EmailTemplateForm(instance=email_template,
                             userObj=None,
                             operation=None)

    if request.method == "POST":
        form = EmailTemplateForm(request.POST,
                                 instance=email_template,
                                 userObj=request.user,
                                 operation='updating')
        if form.is_valid():
            obj = form.save()
            messages.success(request,
                             f'Email Template {obj} successfully updated')
            return redirect('settings:emailTemplateManagement')
        else:
            messages.error(request, 'Invalid form submission')

    context = {'form': form, 'emailTemplate': email_template}
    return render(request, 'templateManagement/emailTemplate.html', context)


@login_required(login_url='company:staffLogin')
@user_passes_test(superuser_check, login_url="permission_error")
def emailTemplateAddPage(request):
    """
    Adding new work template
    """
    form = EmailTemplateForm(userObj=None, operation=None)
    if request.method == "POST":
        form = EmailTemplateForm(request.POST,
                                 userObj=request.user,
                                 operation='creating')
        if form.is_valid():
            obj = form.save()
            messages.success(request,
                             f'Email Template {obj} successfully updated')
            return redirect('settings:emailTemplateManagement')
        else:
            messages.error(request, 'Invalid form submission')

    context = {'form': form}
    return render(request, 'templateManagement/emailTemplateAdd.html', context)


@login_required(login_url='company:staffLogin')
@user_passes_test(superuser_check, login_url="permission_error")
def contractTemplateManagement(request):
    """
    contract Template management page, where you can define the contract
    template that is responsible for contract template creation
    """
    contractTemplates = ContractTemplate.objects.all()
    context = {'contractTemplates': contractTemplates}

    return render(request,
                  'templateManagement/contractTemplateManagement.html',
                  context)


@login_required(login_url='company:staffLogin')
@user_passes_test(superuser_check, login_url="permission_error")
def contractTemplateUpdatePage(request, pk):
    """
    updating the contract template
    """
    contract_template = ContractTemplate.objects.get(pk=pk)
    form = ContractTemplateForm(instance=contract_template,
                                userObj=None,
                                operation=None)

    if request.method == "POST":
        form = ContractTemplateForm(request.POST,
                                    instance=contract_template,
                                    userObj=request.user,
                                    operation='updating')
        if form.is_valid():
            obj = form.save()
            messages.success(request,
                             f'Contract Template {obj} successfully updated')
            return redirect('settings:contractTemplateManagement')
        else:
            messages.error(request, 'Invalid form submission')

    context = {'form': form, 'contractTemplate': contract_template}
    return render(request, 'templateManagement/contractTemplate.html', context)


@login_required(login_url='company:staffLogin')
@user_passes_test(superuser_check, login_url="permission_error")
def contractTemplateAddPage(request):
    """
    Adding new work template
    """
    form = ContractTemplateForm(userObj=None, operation=None)
    if request.method == "POST":
        form = ContractTemplateForm(request.POST,
                                    userObj=request.user,
                                    operation='creating')
        if form.is_valid():
            obj = form.save()
            messages.success(request,
                             f'Contract Template {obj} successfully created')
            return redirect('settings:contractTemplateManagement')
        else:
            messages.error(request, 'Invalid form submission')

    context = {'form': form}
    return render(request, 'templateManagement/contractTemplateAdd.html',
                  context)


@login_required(login_url='company:staffLogin')
@user_passes_test(superuser_check, login_url="permission_error")
def questTemplateManagement(request):
    """
    questionnaire Template management page, where you can define the
    questionnaire template that is responsible for questionnaire template creation
    """
    questTemplates = QuestionnaireTemplate.objects.all()
    context = {'questTemplates': questTemplates}

    return render(request, 'templateManagement/questTemplateManagement.html',
                  context)


@login_required(login_url='company:staffLogin')
@user_passes_test(superuser_check, login_url="permission_error")
def questTemplateUpdatePage(request, pk):
    """
    updating the quest template
    """
    quest_template = QuestionnaireTemplate.objects.get(pk=pk)
    form = QuestionnaireTemplateForm(instance=quest_template,
                                     userObj=None,
                                     operation=None)

    if request.method == "POST":
        form = QuestionnaireTemplateForm(request.POST,
                                         instance=quest_template,
                                         userObj=request.user,
                                         operation='updating')
        if form.is_valid():
            obj = form.save()
            messages.success(
                request, f'Questionnaire Template {obj} successfully updated')
            return redirect('settings:questTemplateManagement')
        else:
            messages.error(request, 'Invalid form submission')

    context = {'form': form, 'questTemplate': quest_template}
    return render(request, 'templateManagement/questTemplate.html', context)


@login_required(login_url='company:staffLogin')
@user_passes_test(superuser_check, login_url="permission_error")
def questTemplateAddPage(request):
    """
    Adding new work template
    """
    form = QuestionnaireTemplateForm(userObj=None, operation=None)
    if request.method == "POST":
        form = QuestionnaireTemplateForm(request.POST,
                                         userObj=request.user,
                                         operation='creating')
        if form.is_valid():
            obj = form.save()
            messages.success(
                request, f'Questionnaire Template {obj} successfully created')
            return redirect('settings:questTemplateManagement')
        else:
            messages.error(request, 'Invalid form submission')

    context = {'form': form}
    return render(request, 'templateManagement/questTemplateAdd.html', context)
