from rest_framework import status, viewsets
from rest_framework.response import Response
from .serializers import AppointmentCreateSerializer


class AppointmentCreateViewSet(viewsets.ViewSet):
    def create(self, request, *args, **kwargs):
        """
        Yangi tayinlash yaratish uchun API.
        Doctor ID va Slot ID qabul qilinadi.
        """
        serializer = AppointmentCreateSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            appointment = serializer.save()
            return Response(
                {
                    "detail": "Tayinlash muvaffaqiyatli yaratildi.",
                    "appointment": AppointmentCreateSerializer(appointment).data
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
