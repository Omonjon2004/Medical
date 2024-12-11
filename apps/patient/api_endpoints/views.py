from rest_framework import generics

from apps.patient \
    .api_endpoints.serializers import (PatientCreateSerializer,
                                       PatientUpdateSerializer,
                                       PatientDetailSerializer,
                                       PatientListSerializer)
from apps.patient.models import Patients
from config.permissions import IsPatientReadOnly

get_queryset = Patients.objects.all()


class PatientCreateAPIView(generics.CreateAPIView):
    queryset = get_queryset
    serializer_class = PatientCreateSerializer
    permission_classes = [IsPatientReadOnly]


class PatientUpdateAPIView(generics.UpdateAPIView):
    queryset = get_queryset
    serializer_class = PatientUpdateSerializer
    permission_classes = [IsPatientReadOnly]


class PatientDeleteAPIView(generics.DestroyAPIView):
    queryset = get_queryset
    serializer_class = PatientDetailSerializer
    permission_classes = [IsPatientReadOnly]


class PatientDetailAPIView(generics.RetrieveAPIView):
    queryset = get_queryset
    serializer_class = PatientDetailSerializer
    permission_classes = [IsPatientReadOnly]


class PatientListAPIView(generics.ListAPIView):
    queryset = get_queryset
    serializer_class = PatientListSerializer
    permission_classes = [IsPatientReadOnly]
