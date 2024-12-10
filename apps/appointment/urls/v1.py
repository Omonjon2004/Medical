# urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.appointment.api_endpoints import AppointmentViewSet

router = DefaultRouter()
router.register(r'appointments', AppointmentViewSet)

urlpatterns = [
    path('', include(router.urls)),]
