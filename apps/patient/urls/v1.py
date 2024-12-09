from django.urls import path

from apps.patient.api_endpoints.views import PatientCreateAPIView, PatientUpdateAPIView, PatientDeleteAPIView, \
    PatientDetailAPIView, PatientListAPIView

urlpatterns = [
    path('list-patients/', PatientListAPIView.as_view(), name='list-patients'),
    path('create-patient', PatientCreateAPIView.as_view(), name='create-patient'),
    path('update-patient/<int:pk>/', PatientUpdateAPIView.as_view(), name='update-patient'),
    path('delete-patient/<int:pk>/', PatientDeleteAPIView.as_view(), name='delete-patient'),
    path('detail-patient/<int:pk>/', PatientDetailAPIView.as_view(), name='detail-patient'),
]
