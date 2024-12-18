from django.urls import path

from apps.medication.api_endpoints import MedicationListAPIView, MedicationCreateAPIView, MedicationUpdateAPIView, \
    MedicationRatingAPIView

urlpatterns = [
    path('medication/<int:pk>/', MedicationUpdateAPIView.as_view(), name='medication-update'),
    path('medication/list/',MedicationListAPIView.as_view(), name='medication-list'),
    path('medication-create/',MedicationCreateAPIView.as_view(), name='medication-create'),
    path('rate-medication/', MedicationRatingAPIView.as_view(), name='rate-medication'),
]