from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from apps.doctor.api_endpoints.doctor_rating_filter.serializers import DoctorFilterSerializer
from apps.doctor.models import Doctors


class DoctorFilterViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = DoctorFilterSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Doctors.objects.all().order_by('-ratings')

