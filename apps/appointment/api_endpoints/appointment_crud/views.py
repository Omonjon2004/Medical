from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

from .serializers import AppointmentSerializer
from ...models import Appointments


class AppointmentViewSet(viewsets.ViewSet):
    queryset = Appointments.objects.all()
    serializer_class = AppointmentSerializer

    def get_queryset(self):
        """
        Foydalanuvchi faqat o'z tayinlashlarini ko'rishiga ruxsat beradi.
        """
        queryset = Appointments.objects.all()
        patient = self.request.user
        queryset = queryset.filter(patient=patient)
        return queryset


    @action(detail=True, methods=['post'])
    def cancel(self, request):
        """
        Tayinlashni bekor qilish.
        """
        try:
            appointment = self.get_object()
            if appointment.patient != request.user:
                return Response(
                    {'detail': 'Siz faqat o\'zingizning '
                               'tayinlashingizni bekor qila olasiz.'},
                    status=status.HTTP_403_FORBIDDEN
                )
            appointment.status = 'Canceled'
            appointment.save()
            return Response({
                'status': 'Appointment canceled successfully'
            }, status=status.HTTP_200_OK)
        except Appointments.DoesNotExist:
            return Response({
                'status': 'Appointment not found'
            }, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['get'])
    def upcoming(self, request):
        """
        Foydalanuvchi uchun upcoming tayinlashlarni olish.
        """
        upcoming_appointments = Appointments.objects.filter(
            patient=request.user, status='Upcoming'
        )
        serializer = self.get_serializer(upcoming_appointments, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def completed(self, request):
        """
        Foydalanuvchi uchun completed tayinlashlarni olish.
        """
        completed_appointments = Appointments.objects.filter(
            patient=request.user, status='Completed'
        )
        serializer = self.get_serializer(
            completed_appointments, many=True
        )
        return Response(serializer.data)
