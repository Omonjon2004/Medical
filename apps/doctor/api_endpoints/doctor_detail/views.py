from rest_framework.generics import RetrieveAPIView
from apps.doctor.models import Doctors
from apps.doctor.api_endpoints.doctor_detail.serializers import DoctorDetailSerializer
from rest_framework.permissions import IsAuthenticated

class DoctorDetailView(RetrieveAPIView):
    queryset = Doctors.objects.all()
    serializer_class = DoctorDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return super().get_queryset().select_related('user').prefetch_related('appointment_slots')

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['date'] = self.request.query_params.get('date', None)
        return context
