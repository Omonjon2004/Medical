from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from apps.doctor.models import Doctors
from .serializers import DoctorFilterSerializer


class DoctorViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    """
    Doctorlarni specialization (kategoriya) bo'yicha filterlash.
    """
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'specialization',
                openapi.IN_QUERY,
                description="Doctorni specialization bo'yicha filterlash",
                type=openapi.TYPE_STRING
            )
        ],
        responses={200: DoctorFilterSerializer(many=True)}
    )
    def list(self, request):
        """
        GET: Doctorlar ro'yxati, specialization bo'yicha filterlash va ratings bo'yicha kamayish tartibida chiqarish.
        """
        specialization = request.query_params.get('specialization', None)
        query = Doctors.objects.all()

        # Specialization bo'yicha filterlash
        if specialization:
            query = query.filter(specialization__iexact=specialization)

        # Ratings bo'yicha kamayish tartibida saralash
        doctors = query.order_by('-ratings')
        serializer = DoctorFilterSerializer(doctors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def specializations_list(self, request):
        """
        Takrorlanmas specializationlarni chiqaradi.
        """
        specializations = Doctors.objects.values_list('specialization', flat=True).distinct()
        return Response({"specializations": list(specializations)}, status=status.HTTP_200_OK)
