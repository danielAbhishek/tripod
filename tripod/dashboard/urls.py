from django.urls import path

from dashboard import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboarHome, name='dashboardHome'),
    path('download_summary',
         views.download_summary_report,
         name='download_summary'),
]
