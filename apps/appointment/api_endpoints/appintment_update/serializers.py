from rest_framework import serializers
from apps.appointment.models import Appointments
from apps.doctor.models import AppointmentSlot

class AppointmentUpdateSerializer(serializers.ModelSerializer):
    slot_id = serializers.PrimaryKeyRelatedField(queryset=AppointmentSlot.objects.all(), help_text="Slot ID sini kiriting")

    class Meta:
        model = Appointments
        fields = ['id', 'slot_id']  # Appointment ID va Slot ID

    def validate(self, data):
        slot = data.get('slot_id')

        # Slot bo'sh ekanligini tekshirish
        if slot is None:
            raise serializers.ValidationError("Slot is required.")

        # Slot va doktor band bo'lmaganligini tekshirish
        if Appointments.objects.filter(slot=slot, date=data.get('date')).exists():
            raise serializers.ValidationError(f"The selected slot is already taken by another appointment.")

        return data
