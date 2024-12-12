# views.py

from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

from apps.doctor.models import AppointmentSlot, Doctors
from .serializers import AppointmentSerializer
from ...models import Appointments


class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointments.objects.all()
    serializer_class = AppointmentSerializer

    def get_queryset(self):
        """
        Foydalanuvchi faqat o'z tayinlashlarini ko'rishiga ruxsat beradi.
        """
        queryset = Appointments.objects.all()
        patient = self.request.user  # Hozirgi foydalanuvchi (patient)
        queryset = queryset.filter(patient=patient)
        return queryset

    def create(self, request, *args, **kwargs):
        doctor_id = request.data.get('doctor')
        slot_id = request.data.get('slot')

        if not doctor_id or not slot_id:
            return Response(
                {"detail": "Doctor va slot ma'lumotlari kerak."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            doctor = Doctors.objects.get(id=doctor_id)
            slot = AppointmentSlot.objects.get(id=slot_id)
        except Doctors.DoesNotExist:
            return Response(
                {"detail": "Doctor topilmadi."},
                status=status.HTTP_400_BAD_REQUEST
            )
        except AppointmentSlot.DoesNotExist:
            return Response(
                {"detail": "Slot topilmadi."},
                status=status.HTTP_400_BAD_REQUEST
            )

        existing_appointment = Appointments.objects.filter(
            doctor=doctor, slot=slot
        ).first()
        if existing_appointment:
            return Response(
                {"detail": "Bu doktor va slot"
                           " kombinatsiyasiga allaqachon bemor tayinlangan."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Patientni o'zgaruvchi sifatida aniqlaymiz
        request.data['patient'] = request.user.id
        return super().create(request, *args, **kwargs)

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
