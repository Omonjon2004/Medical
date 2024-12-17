from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from apps.appointment.api_endpoints.appintment_update.serializers import AppointmentRescheduleSerializer
from apps.appointment.models import Appointments
from apps.appointment.api_endpoints import AppointmentCreateSerializer


class AppointmentUpdateView(viewsets.ViewSet):
    """
    Tayinlashlarni yangilash (Reschedule) API
    """

    @action(detail=False, methods=['patch'], url_path='reschedule')
    @swagger_auto_schema(request_body=AppointmentRescheduleSerializer)
    def reschedule(self, request):
        """
        Tayinlashni qayta belgilash (Reschedule).

        `appointment_id` va `new_slot`ni JSON formatida qabul qilamiz.
        """
        serializer = AppointmentRescheduleSerializer(data=request.data)

        if serializer.is_valid():
            appointment_id = serializer.validated_data['appointment_id']
            new_slot_id = serializer.validated_data['new_slot']

            try:
                appointment = Appointments.objects.get(pk=appointment_id, patient=request.user)
            except Appointments.DoesNotExist:
                return Response(
                    {"detail": "Tayinlash topilmadi yoki sizga tegishli emas."},
                    status=status.HTTP_404_NOT_FOUND
                )

            updated_appointment = serializer.update(appointment, serializer.validated_data)

            return Response(
                {
                    "detail": "Tayinlash muvaffaqiyatli yangilandi (Rescheduled).",
                    "appointment": AppointmentCreateSerializer(updated_appointment).data
                },
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
