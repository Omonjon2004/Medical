from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import AppointmentSerializer
from rest_framework.permissions import IsAuthenticated

from ...models import Appointments


class AppointmentViewSet(viewsets.ViewSet):
    """
    ViewSet for managing appointments with custom actions.
    """
    permission_classes = [IsAuthenticated]

    def list(self, request):
        appointments = Appointments.objects.filter(patient=request.user)
        serializer = AppointmentSerializer(appointments, many=True)
        return Response(serializer.data)

    # Bitta appointmentni olish
    def retrieve(self, request, pk=None):
        try:
            appointment = Appointments.objects.get(pk=pk, patient=request.user)
        except Appointments.DoesNotExist:
            return Response({"error": "Appointment not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = AppointmentSerializer(appointment)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='upcoming')
    def upcoming(self, request):
        appointments = Appointments.objects.filter(patient=request.user, status='Upcoming')
        serializer = AppointmentSerializer(appointments, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='completed')
    def completed(self, request):
        appointments = Appointments.objects.filter(patient=request.user, status='Completed')
        serializer = AppointmentSerializer(appointments, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='canceled')
    def canceled(self, request):
        appointments = Appointments.objects.filter(patient=request.user, status='Canceled')
        serializer = AppointmentSerializer(appointments, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_path='cancel')
    def cancel(self, request, pk=None):
        try:
            appointment = Appointments.objects.get(pk=pk, patient=request.user)
            appointment.status = 'Canceled'
            appointment.save()
            return Response({"status": "Appointment canceled successfully."})
        except Appointments.DoesNotExist:
            return Response({"error": "Appointment not found."}, status=status.HTTP_404_NOT_FOUND)
