# urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.appointment.api_endpoints import AppointmentCreateViewSet

router = DefaultRouter()
router.register(r'create', AppointmentCreateViewSet, basename='create')

urlpatterns = [
    path('', include(router.urls)),]
