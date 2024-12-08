from django.urls import path

from apps.doctor.api_endpoints import DoctorCreateAPIView, DoctorUpdateAPIView, DoctorListAPIView, DoctorDestroyAPIView, \
    DoctorDetailAPIView, DoctorFilterViewSet, DoctorSearchSerializer, DoctorSearchAPIView

urlpatterns = [
    path('list-doctors/', DoctorListAPIView.as_view(), name='list_doctors'),
    path('create-doctor/', DoctorCreateAPIView.as_view(), name='create_doctor'),
    path('update-doctor/<int:pk>/', DoctorUpdateAPIView.as_view(), name='update_doctor'),
    path('delete-doctor/<int:pk>/',DoctorDestroyAPIView.as_view(), name='delete_doctor'),
    path('detail-doctor/<int:pk>/', DoctorDetailAPIView.as_view(), name='detail_doctor'),
    path('doctor-rating-filter/', DoctorFilterViewSet.as_view({'get': 'list'}), name='doctor_rating_filter'),
    path('doctor-search/', DoctorSearchAPIView.as_view(), name='doctor_search'),
]
