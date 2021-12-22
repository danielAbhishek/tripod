from django.urls import path

from core import views

urlpatterns = [
    path('accounts/register/', views.registerPage, name='register'),
    path('accounts/login/', views.loginPage, name='login'),
    path('accounts/logout/', views.logoutPage, name='logout'),
    path('', views.home, name='home'),
]
