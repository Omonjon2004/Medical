from rest_framework.generics import (
    CreateAPIView, ListAPIView, UpdateAPIView, DestroyAPIView)

from apps.doctor.api_endpoints.doctor_crud.serializers import (
    DoctorCreateSerializer, DoctorUpdateSerializer,
    DoctorListSerializer, DoctorDetailSerializer, )
from apps.doctor.models import Doctors

get_queryset = Doctors.objects.all()


class DoctorCreateAPIView(CreateAPIView):
    serializer_class = DoctorCreateSerializer
    queryset = Doctors.objects.all()

    def perform_create(self, serializer):
        # Foydalanuvchi faqat serializerga uzatiladi
        serializer.save(user=self.request.user)


class DoctorUpdateAPIView(UpdateAPIView):
    serializer_class = DoctorUpdateSerializer
    queryset = get_queryset


class DoctorListAPIView(ListAPIView):
    queryset = get_queryset
    serializer_class = DoctorListSerializer


class DoctorDestroyAPIView(DestroyAPIView):
    serializer_class = DoctorDetailSerializer
    queryset = get_queryset
