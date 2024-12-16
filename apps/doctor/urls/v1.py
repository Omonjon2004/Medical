from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.doctor.api_endpoints import DoctorCreateAPIView, DoctorUpdateAPIView, DoctorListAPIView, DoctorDestroyAPIView, \
 DoctorSearchAPIView, DoctorDetailView
from apps.doctor.api_endpoints.specialization_filter.views import DoctorViewSet

router = DefaultRouter()
router.register(r'filter', DoctorViewSet, basename='doctors')

urlpatterns = [
    path('', include(router.urls)),

    path('list-doctors/', DoctorListAPIView.as_view({'get': 'list'}), name='list_doctors'),
    path('create-doctor/', DoctorCreateAPIView.as_view(), name='create_doctor'),
    path('update-doctor/<int:pk>/', DoctorUpdateAPIView.as_view(), name='update_doctor'),
    path('delete-doctor/<int:pk>/',DoctorDestroyAPIView.as_view(), name='delete_doctor'),
    path('doctor-search/', DoctorSearchAPIView.as_view(), name='doctor_search'),
    path('doctor/<int:pk>/details/', DoctorDetailView.as_view(), name='doctor-detail'),
]