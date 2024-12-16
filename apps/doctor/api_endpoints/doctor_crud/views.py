from rest_framework import viewsets
from rest_framework.generics import (
    CreateAPIView, ListAPIView, UpdateAPIView, DestroyAPIView)
from rest_framework.permissions import IsAuthenticated

from apps.doctor.api_endpoints.doctor_crud.serializers import (
    DoctorCreateSerializer, DoctorUpdateSerializer,
    DoctorListSerializer, DoctorDetailSerializer, )
from apps.doctor.models import Doctors
from config.permissions import IsDoctorReadOnly

get_queryset = Doctors.objects.all()


class DoctorCreateAPIView(CreateAPIView):
    serializer_class = DoctorCreateSerializer
    queryset = Doctors.objects.all()
    permission_classes = [IsDoctorReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class DoctorUpdateAPIView(UpdateAPIView):
    serializer_class = DoctorUpdateSerializer
    queryset = get_queryset
    permission_classes = [IsDoctorReadOnly]



class DoctorListAPIView(viewsets.ReadOnlyModelViewSet):
    serializer_class = DoctorListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Doctors.objects.all().order_by('-ratings')


class DoctorDestroyAPIView(DestroyAPIView):
    serializer_class = DoctorDetailSerializer
    queryset = get_queryset
    permission_classes = [IsDoctorReadOnly]
