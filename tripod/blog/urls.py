from django.urls import path, include

from blog import views

app_name = 'blog'


urlpatterns = [
    path('', views.registerPage, name='customerRegister'),
]
