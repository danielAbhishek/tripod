from django.urls import path

from company import views

app_name = 'company'

urlpatterns = [
    # company pages urls
    path('', views.staffCompanyHomePage, name='staffCompany'),
    path('login/', views.staffLoginPage, name='staffLogin'),
    path('logout/', views.staffLogoutPage, name='staffLogout'),

    # Employee management
    path(
        'employeeManagement',
        views.employeeManagementPage,
        name='employeeManagement'),
    path(
        'employeeManagement/employee/<int:pk>',
        views.staffUpdatePage, name='employeeUpdatePage'),
    path(
        'employeeManagement/employee/add/',
        views.staffAddPage, name='employeeAdd'),

    # User management
    path(
        'clientManagement',
        views.clientManagementPage,
        name='clientManagement'),
    path(
        'clientManagement/client/<int:pk>',
        views.clientUpdatePage,
        name='clientUpdatePage'),
    path(
        'clientManagement/client/add/',
        views.clientAddPage, name='clientAdd'),

    # Event management
    path(
        'packageManagement/events', views.eventManagement,
        name='eventManagement'),
    path(
        'packageManagement/event/add/', views.eventAddPage,
        name='eventAdd'),
    path(
        'packageManagement/event/<int:pk>', views.eventUpdatePage,
        name='eventUpdate'),

    # Product Management
    path(
        'packageManagement/products', views.productManagement,
        name='productManagement'),
    path(
        'packageManagement/product/add/', views.productAddPage,
        name='productAdd'),
    path(
        'packageManagement/product/<int:pk>', views.productUpdatePage,
        name='productUpdate'),

    # package Management
    path(
        'packageManagement/packages', views.packageManagement,
        name='packageManagement'),
    path(
        'packageManagement/package/add/', views.packageAddPage,
        name='packageAdd'),
    path(
        'packageManagement/package/<int:pk>', views.packageUpdatePage,
        name='packageUpdate'),

]
