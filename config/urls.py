"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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

# Swagger URL-larini qo'shish
from config.swagger import swagger_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('apps.account_.urls.v1')),
    path('api/userprofile/', include('apps.account_.urls.v2')),
    path('api/user/activation', include('apps.account_.urls.v3')),
    path('api/doctor/', include('apps.doctor.urls.v1')),
    path('api/patient/', include('apps.patient.urls.v1')),
    path('api/medication/', include('apps.medication.urls.v1')),
    path('api/basket/', include('apps.basket.urls.v1')),
]

urlpatterns += swagger_urlpatterns


