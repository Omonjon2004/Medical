from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import DoctorSerializer
from ...models import Doctors


class DoctorViewSet(viewsets.ViewSet):
    """
    Doctorlarni specialization (kategoriya) bo'yicha filterlash.
    """
    def list(self, request):
        """
        Doctorlar ro'yxati. Specialization (kategoriya) bo'yicha filterlash uchun `specialization` query parametri ishlatiladi.
        Misol: /doctors/?specialization=Cardiologist
        """
        specialization = request.query_params.get('specialization', None)
        doctors = Doctors.objects.all()

        if specialization:
            doctors = doctors.filter(specialization__iexact=specialization)

        serializer = DoctorSerializer(doctors, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def specializations(self, request):
        """
        Specialization (kategoriya) bo'yicha barcha unikal qiymatlarni qaytarish.
        """
        specializations = Doctors.objects.values_list('specialization', flat=True).distinct()
        return Response(list(specializations))