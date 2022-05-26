from django.urls import path

from company import views

app_name = 'company'

urlpatterns = [
    # company pages urls
    path('', views.staffCompanyHomePage, name='staffCompany'),
    path('login/', views.staffLoginPage, name='staffLogin'),
    path('logout/', views.staffLogoutPage, name='staffLogout'),
    path('<int:pk>', views.companyUpdate, name='companyUpdate'),
    path('account', views.updateProfile, name='updateProfile'),
    path('account/change_password',
         views.changePassword,
         name='changePassword'),
    # Employee management
    path('employeeManagement',
         views.employeeManagementPage,
         name='employeeManagement'),
    path('employeeManagement/employee/<int:pk>',
         views.staffUpdatePage,
         name='employeeUpdatePage'),
    path('clientManagement/employee/delete/<int:pk>',
         views.userDeletePage,
         name='employeeDeletePage'),
    path('employeeManagement/employee/add/',
         views.staffAddPage,
         name='employeeAdd'),

    # User management
    path('clientManagement',
         views.clientManagementPage,
         name='clientManagement'),
    path('clientManagement/client/<int:pk>',
         views.clientUpdatePage,
         name='clientUpdatePage'),
    path('clientManagement/client/delete/<int:pk>',
         views.userDeletePage,
         name='clientDeletePage'),
    path('clientManagement/client/add/', views.clientAddPage,
         name='clientAdd'),

    # Event management
    path('packageManagement/events',
         views.eventManagement,
         name='eventManagement'),
    path('packageManagement/event/add/', views.eventAddPage, name='eventAdd'),
    path('packageManagement/event/<int:pk>',
         views.eventUpdatePage,
         name='eventUpdate'),
    path('packageManagement/event/delete/<int:pk>',
         views.eventDeletePage,
         name='eventDelete'),

    # Product Management
    path('packageManagement/products',
         views.productManagement,
         name='productManagement'),
    path('packageManagement/product/add/',
         views.productAddPage,
         name='productAdd'),
    path('packageManagement/product/<int:pk>',
         views.productUpdatePage,
         name='productUpdate'),
    path('packageManagement/product/delete/<int:pk>',
         views.productDeletePage,
         name='productDelete'),

    # package Management
    path('packageManagement/packages',
         views.packageManagement,
         name='packageManagement'),
    path('packageManagement/package/add/',
         views.packageAddPage,
         name='packageAdd'),
    path('packageManagement/package/<int:pk>',
         views.packageUpdatePage,
         name='packageUpdate'),

    # finance Management
    path('finance/invoices', views.invoiceManagement,
         name='invoiceManagement'),
    path('finance/invoice/<int:pk>', views.invoiceDetail,
         name='invoiceDetail'),
    path('finance/invoice/delete/<int:pk>', views.invoiceDeletePage,
         name='invoiceDeletePage'),

    # Equipment management
    path('equipmentManagement/equipments',
         views.equipmentManagement,
         name='equipmentManagement'),
    path('equipmentManagement/equipment/add/',
         views.equipmentAddPage,
         name='equipmentAdd'),
    path('equipmentManagement/equipment/<int:pk>',
         views.equipmentUpdatePage,
         name='equipmentUpdate'),
    path('equipmentManagement/equipment/delete/<int:pk>',
         views.equipmentDeletePage,
         name='equipmentDeletePage'),


    # Equipment maintanence
    path('equipmentMaintanence/equipments',
         views.equipmentMaintanence,
         name='equipmentMaintanence'),
    path('equipmentMaintanence/equipment/add/',
         views.equipmentMaintanenceAddPage,
         name='equipmentMaintanenceAdd'),
    path('equipmentMaintanence/equipment/<int:pk>',
         views.equipmentMaintanenceUpdatePage,
         name='equipmentMaintanenceUpdate'),
    path('equipmentMaintanence/equipment/delete/<int:pk>',
         views.equipmentMaintanenceDeletePage,
         name='equipmentMaintanenceDeletePage'),
]
