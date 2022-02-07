from django.urls import path

from core import views

app_name = 'core'

urlpatterns = [
    # customer/users pages urls
    path('', views.home, name='home'),
    path('accounts/register/', views.registerPage, name='register'),
    path('accounts/login/', views.loginPage, name='login'),
    path('accounts/logout/', views.logoutPage, name='logout'),
]
