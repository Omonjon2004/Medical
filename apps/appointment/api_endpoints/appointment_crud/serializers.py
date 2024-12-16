from rest_framework import serializers

from apps.appointment.models import Appointments


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointments
        fields = [
            'id',
            'doctor',
            'slot',
            'status',
            'confirmed',
            'created_at'
        ]
