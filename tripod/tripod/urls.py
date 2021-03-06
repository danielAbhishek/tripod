"""tripod URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from tripod.views import not_available_404, permission_error, admin_page
from tripod import settings

from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('error', not_available_404, name="error"),
    path('permission_error', permission_error, name="permission_error"),
    path('', include('core.urls')),
    path('blog/', include('blog.urls')),
    path('tripod-admin/', admin_page, name='adminPage'),
    path('tripod-admin/dashboard/', include('dashboard.urls')),
    path('tripod-admin/company/', include('company.urls')),
    path('tripod-admin/job/', include('job.urls')),
    path('tripod-admin/settings/', include('settings.urls')),
    # path('tripod-admin/...', include('settings.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
