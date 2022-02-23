from django.urls import path

from job import views

app_name = 'job'

urlpatterns = [
    path('', views.staffJobHomePage, name='staffJob'),

    # job management
    path(
        'jobReqManagement',
        views.jobReqManagementPage, name='jobReqManagementPage'),
    path(
        'jobReqManagement/jobReq/add/',
        views.jobReqAddPage, name='jobReqAdd'),
    path(
        'jobReqManagement/reqToJob/<int:pk>/',
        views.jobChangeReqToJob, name='jobChangeReqToJobPage'),

    path(
        'jobManagement',
        views.jobManagementPage, name='jobManagementPage'),
    path(
        'jobManagement/job/<int:pk>',
        views.jobPage, name='jobPage'),
    path(
        'jobManagement/jobUpdate/<int:pk>/',
        views.jobUpdateJob, name='jobUpdateJob'),

    path(
        'jobManagement/workProcess/<int:pk>',
        views.completeWork, name='processWork'),
]
