from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.appointment.api_endpoints.appointment_crud import AppointmentViewSet

router = DefaultRouter()
router.register(r'crud', AppointmentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
