from django.urls import path

from apps.medication.api_endpoints import MedicationListAPIView
from apps.medication.api_endpoints.views import MedicationsRetrieveUpdateDestroyAPIView, MedicationsCreateAPIView

urlpatterns = [
    path('medication/<int:pk>/', MedicationsRetrieveUpdateDestroyAPIView.as_view(), name='medication-detail'),
    path('medication/create/', MedicationsCreateAPIView.as_view(), name='medication-create'),
    path('medication/list/',MedicationListAPIView.as_view(), name='medication-list'),
]