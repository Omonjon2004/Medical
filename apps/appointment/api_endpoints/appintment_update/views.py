from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status

from apps.appointment.api_endpoints.appintment_update.serializers import AppointmentUpdateSerializer
from apps.appointment.models import Appointments


class AppointmentUpdateView(viewsets.ViewSet):
    """
    A ViewSet for performing CRUD operations on Appointments.
    """


    def update(self, request, pk=None):
        """
        Update an existing appointment.
        """
        try:
            appointment = Appointments.objects.get(pk=pk)
        except Appointments.DoesNotExist:
            return Response({"detail": "Appointment not found."}, status=status.HTTP_404_NOT_FOUND)

        # Deserialize the incoming data and validate
        serializer = AppointmentUpdateSerializer(appointment, data=request.data, partial=True)

        if serializer.is_valid():
            slot = serializer.validated_data.get('slot_id', None)
            if slot:
                # Check if the slot is already taken by another appointment on the same day
                if Appointments.objects.filter(slot=slot, date=appointment.date).exists():
                    return Response(
                        {"detail": "The selected slot is already taken by another appointment."},
                        status=status.HTTP_400_BAD_REQUEST
                    )

            # If validation passed, save the changes
            serializer.save()

            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['put'], url_path='custom-update')
    def custom_update(self, request, pk=None):
        """
        Custom update for the appointment (can be used for custom validation).
        """
        try:
            appointment = Appointments.objects.get(pk=pk)
        except Appointments.DoesNotExist:
            return Response({"detail": "Appointment not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = AppointmentUpdateSerializer(appointment, data=request.data, partial=True)

        if serializer.is_valid():
            slot = serializer.validated_data.get('slot_id', None)
            if slot:
                # Additional slot validation
                if Appointments.objects.filter(slot=slot, date=appointment.date).exists():
                    return Response(
                        {"detail": "The selected slot is already taken by another appointment."},
                        status=status.HTTP_400_BAD_REQUEST
                    )

            # Save if everything is okay
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

