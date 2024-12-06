from rest_framework import generics

from apps.patient.api_endpoints.serializers import PatientCreateSerializer, PatientUpdateSerializer, \
    PatientDetailSerializer, PatientListSerializer
from apps.patient.models import Patients

get_queryset = Patients.objects.all()


class PatientCreateAPIView(generics.CreateAPIView):
    queryset = get_queryset
    serializer_class = PatientCreateSerializer


class PatientUpdateAPIView(generics.UpdateAPIView):
    queryset = get_queryset
    serializer_class = PatientUpdateSerializer

class PatientDeleteAPIView(generics.DestroyAPIView):
    queryset = get_queryset
    serializer_class = PatientDetailSerializer

class PatientDetailAPIView(generics.RetrieveAPIView):
    queryset = get_queryset
    serializer_class = PatientDetailSerializer

class PatientListAPIView(generics.ListAPIView):
    queryset = get_queryset
    serializer_class = PatientListSerializer