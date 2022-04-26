from django.urls import path

from job import views

app_name = 'job'

urlpatterns = [
    path('', views.staffJobHomePage, name='staffJob'),

    # job request management
    path('jobReqManagement',
         views.jobReqManagementPage,
         name='jobReqManagementPage'),
    path('jobReqManagement/jobReq/add/', views.jobReqAddPage,
         name='jobReqAdd'),
    path('jobReqManagement/reqToJob/<int:pk>/',
         views.jobChangeReqToJob,
         name='jobChangeReqToJobPage'),

    # job management
    path('jobManagement', views.jobManagementPage, name='jobManagementPage'),
    path('jobManagement/job/<int:pk>', views.jobPage, name='jobPage'),
    path('jobManagement/jobUpdate/<int:pk>/',
         views.jobUpdateJob,
         name='jobUpdateJob'),
    path('jobManagement/taskProcess/<int:pk>',
         views.processTask,
         name='processTask'),
    path('jobManagement/taskComplete/<int:pk>',
         views.completeTask,
         name='completeTask'),
    # invoice
    path('jobManagement/jobUpdate/<int:pk>/invoice',
         views.updateInvoice,
         name='jobUpdateInvoice'),
    path('jobManagement/job/<int:pk>/invoice',
         views.invoicePage,
         name='invoicePage'),
    path('jobManagement/job/<int:pk>/PayHistory/',
         views.addPayHistoryPage,
         name='addPayHistoryPage'),
    path('jobManagement/job/<int:pk>/updatePayHistory/',
         views.updatePayHistoryPage,
         name='updatePayHistoryPage'),
    # quest
    path('jobManagement/job/<int:pk>/questonniare',
         views.questPage,
         name='questPage'),

    # job declined management
    path('jobDecManagement',
         views.jobDecManagementPage,
         name='jobDecManagementPage'),

    # appointment management
    path('taskManagement/app/<int:pk>', views.appointmentPage, name='appPage'),
]
