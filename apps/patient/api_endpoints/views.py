from rest_framework import generics
from rest_framework.permissions import IsAdminUser

from apps.patient \
    .api_endpoints.serializers import (PatientCreateSerializer,
                                       PatientUpdateSerializer,
                                       PatientDetailSerializer,
                                       PatientListSerializer)
from apps.patient.models import Patients
from config.permissions import IsPatientReadOnly




class PatientCreateAPIView(generics.CreateAPIView):
    queryset = Patients.objects.all()
    serializer_class = PatientCreateSerializer
    permission_classes = [IsAdminUser]


class PatientUpdateAPIView(generics.UpdateAPIView):
    queryset = Patients.objects.all()
    serializer_class = PatientUpdateSerializer
    permission_classes = [IsAdminUser]


class PatientDeleteAPIView(generics.DestroyAPIView):
    queryset = Patients.objects.all()
    serializer_class = PatientDetailSerializer
    permission_classes = [IsAdminUser]


class PatientDetailAPIView(generics.RetrieveAPIView):
    queryset = Patients.objects.all()
    serializer_class = PatientDetailSerializer
    permission_classes = [IsAdminUser]


class PatientListAPIView(generics.ListAPIView):
    queryset = Patients.objects.all()
    serializer_class = PatientListSerializer
    permission_classes = [IsAdminUser]
