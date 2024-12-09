from django.urls import path

from apps.medication.api_endpoints import MedicationListAPIView, MedicationAddUpdateView
from apps.medication.api_endpoints.views import MedicationsRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('medication/<int:pk>/', MedicationsRetrieveUpdateDestroyAPIView.as_view(), name='medication-detail'),
    path('medication/list/',MedicationListAPIView.as_view(), name='medication-list'),
    path('medication-create/',MedicationAddUpdateView.as_view(), name='medication-create'),
]