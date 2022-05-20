from django.urls import path, include

from blog import views

app_name = 'blog'

urlpatterns = [
    path('', views.tripodPage, name='tripodPage'),
    path('contact', views.contactPage, name='contactUs'),
    path('features', views.featuresPage, name='features'),
]
