from django.urls import path

from core import views

app_name = 'core'

urlpatterns = [
    # account pages urls
    path('', views.home, name='home'),
    path('accounts/change_password',
         views.changePassword,
         name='changePassword'),
    path('accounts/login/', views.loginPage, name='login'),
    path('accounts/logout/', views.logoutPage, name='logout'),

    # customer portal
    path('portal/', views.customerHome, name='customerHome'),

    # jobs
    path('portal/jobRequests/', views.jobRequests, name='jobRequests'),
    path('portal/jobRequests/add/', views.jobReqAddPage, name='jobReqAdd'),
    path('portal/jobs/', views.jobsConfirmed, name='jobs'),
    path('portal/declinedJobs/', views.jobsDeclined, name='declinedJobs'),
    path('portal/job/<int:pk>', views.jobPage, name='jobPage'),
    path('portal/updateJob/<int:pk>', views.jobUpdate, name='jobUpdate'),
    path('portal/updatePackage/<int:pk>',
         views.jobUpdatePackage,
         name='jobUpdatePackage'),
    path('portal/taskComplete/<int:pk>',
         views.completeTask,
         name='completeTask'),
    path('portal/job/contract/<int:pk>',
         views.contractPage,
         name='jobContract'),
    path('portal/job/invoice/<int:pk>', views.invoicePage, name='jobInvoice'),
    path('portal/job/quest/<int:pk>',
         views.updateQuestForm,
         name='updateQuestForm'),
]
