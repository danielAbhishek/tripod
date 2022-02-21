from django.urls import path

from settings import views

app_name = 'settings'

urlpatterns = [
    # company pages urls
    path('', views.staffSettingsPage, name='staffSettings'),

    # workflow Management
    path(
        'workflowManagement',
        views.workflowManagement, name='workflowManagement'),
    path(
        'workflowManagement/workflow/<int:pk>',
        views.workflowUpdatePage, name='workflowUpdatePage'),
    path(
        'workflowManagement/workflow/add/',
        views.workflowAddPage, name='workflowAdd'),

    # work Templates management
    path(
        'workTemplateManagement',
        views.workTemplateManagement, name='workTemplateManagement'),
    path(
        'workTemplateManagement/workTemplate/<int:pk>',
        views.workTemplateUpdatePage, name='workTemplateUpdatePage'),
    path(
        'workTemplateManagement/workTemplate/add/',
        views.workTemplateAddPage, name='workTemplateAdd'),

    # email template management
    path(
        'emailTemplateManagement',
        views.emailTemplateManagement, name='emailTemplateManagement'),
    path(
        'emailTemplateManagement/emailTemplate/<int:pk>',
        views.emailTemplateUpdatePage, name='emailTemplateUpdatePage'),
    path(
        'emailTemplateManagement/emailTemplate/add/',
        views.emailTemplateAddPage, name='emailTemplateAdd'),

    # Contract template management
    path(
        'contractTemplateManagement',
        views.contractTemplateManagement, name='contractTemplateManagement'),
    path(
        'contractTemplateManagement/contractTemplate/<int:pk>',
        views.contractTemplateUpdatePage, name='contractTemplateUpdatePage'),
    path(
        'contractTemplateManagement/contractTemplate/add/',
        views.contractTemplateAddPage, name='contractTemplateAdd'),

    # Questionnaire template management
    path(
        'questTemplateManagement',
        views.questTemplateManagement, name='questTemplateManagement'),
    path(
        'questTemplateManagement/questTemplate/<int:pk>',
        views.questTemplateUpdatePage, name='questTemplateUpdatePage'),
    path(
        'questTemplateManagement/questTemplate/add/',
        views.questTemplateAddPage, name='questTemplateAdd'),
    # sources management
]
