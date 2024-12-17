from rest_framework import serializers
from apps.appointment.models import Appointments
from apps.doctor.models import AppointmentSlot


class AppointmentRescheduleSerializer(serializers.Serializer):
    appointment_id = serializers.IntegerField(required=True, help_text="Tayinlash ID (Appointment ID) ni kiriting")
    new_slot = serializers.PrimaryKeyRelatedField(
        queryset=AppointmentSlot.objects.all(),
        required=True,
        help_text="Yangi slot ID ni kiriting"
    )

    def validate(self, data):
        appointment_id = data.get('appointment_id')
        new_slot = data.get('new_slot')

        try:
            appointment = Appointments.objects.get(pk=appointment_id)
        except Appointments.DoesNotExist:
            raise serializers.ValidationError({"appointment_id": "Tayinlash topilmadi."})

        if new_slot.doctor != appointment.doctor:
            raise serializers.ValidationError(
                {"new_slot": "Yangi slot tanlangan doktorga tegishli emas."}
            )

        if not new_slot.is_available:
            raise serializers.ValidationError(
                {"new_slot": "Yangi slot allaqachon band qilingan."}
            )

        return data

    def update(self, instance, validated_data):
        old_slot = instance.slot
        old_slot.is_available = True
        old_slot.save()

        new_slot = validated_data['new_slot']
        new_slot.is_available = False
        new_slot.save()

        instance.slot = new_slot
        instance.save()
        return instance
