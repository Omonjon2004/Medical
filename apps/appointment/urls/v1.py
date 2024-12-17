# urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.appointment.api_endpoints import AppointmentCreateViewSet
from apps.appointment.api_endpoints.appintment_update import AppointmentUpdateView
from apps.appointment.api_endpoints.appointment_crud import AppointmentViewSet

router = DefaultRouter()
router.register(r'create', AppointmentCreateViewSet, basename='create')
router.register(r'crud', AppointmentViewSet, basename='crud')
router.register(r'reschedule', AppointmentUpdateView, basename='reschedule')

urlpatterns = [
    path('', include(router.urls)),
]
