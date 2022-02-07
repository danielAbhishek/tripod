from django.urls import path

from company import views

app_name = 'company'

urlpatterns = [
    # company pages urls
    path('company/', views.staffCompanyHomePage, name='staffCompany'),
    path('login/', views.staffLoginPage, name='staffLogin'),
    path('logout/', views.staffLogoutPage, name='staffLogout'),

    # Employee management
    path(
        'company/employeeManagement',
        views.employeeManagementPage,
        name='employeeManagement'),
    path(
        'company/employeeManagement/employee/<int:pk>',
        views.staffUpdatePage, name='employeeUpdatePage'),
    path(
        'company/employeeManagement/employee/add/',
        views.staffAddPage, name='employeeAdd'),

    # User management
    path(
        'company/clientManagement',
        views.clientManagementPage,
        name='clientManagement'),
    path(
        'company/clientManagement/client/<int:pk>',
        views.clientUpdatePage,
        name='clientUpdatePage'),
    path(
        'company/clientManagement/client/add/',
        views.clientAddPage, name='clientAdd'),

    # Event management
    path(
        'company/packageManagement/events', views.eventManagement,
        name='eventManagement'),
    path(
        'company/packageManagement/event/add/', views.eventAddPage,
        name='eventAdd'),
    path(
        'company/packageManagement/event/<int:pk>', views.eventUpdatePage,
        name='eventUpdate'),

    # Product Management
    path(
        'company/packageManagement/products', views.productManagement,
        name='productManagement'),
    path(
        'company/packageManagement/product/add/', views.productAddPage,
        name='productAdd'),
    path(
        'company/packageManagement/product/<int:pk>', views.productUpdatePage,
        name='productUpdate'),

    # package Management
    path(
        'company/packageManagement/packages', views.packageManagement,
        name='packageManagement'),
    path(
        'company/packageManagement/package/add/', views.packageAddPage,
        name='packageAdd'),
    path(
        'company/packageManagement/package/<int:pk>', views.packageUpdatePage,
        name='packageUpdate'),

]
