from django.utils import timezone
from drf_yasg import openapi
from rest_framework.generics import RetrieveAPIView

from apps.doctor.models import Doctors
from apps.doctor.api_endpoints.doctor_detail.serializers import DoctorDetailSerializer
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
class DoctorDetailView(RetrieveAPIView):
    queryset = Doctors.objects.all()
    serializer_class = DoctorDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Querysetni select_related va prefetch_related yordamida optimallashtirish
        return super().get_queryset().select_related('user').prefetch_related('appointment_slots')

    def get_serializer_context(self):
        # Serializer contextiga 'date' query parametrini qo'shish
        context = super().get_serializer_context()
        context['date'] = self.request.query_params.get('date', None)
        return context

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'date',
                openapi.IN_QUERY,
                description="Kutilgan sanani kiriting (format: YYYY-MM-DD)",
                type=openapi.TYPE_STRING,
                required=False,  # endi bu parametr majburiy emas
                default=timezone.localtime(timezone.now()).date().isoformat()  # Hozirgi sanani default qiymat sifatida berish
            )
        ]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)