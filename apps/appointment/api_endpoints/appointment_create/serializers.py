from django.db.models import IntegerField
from rest_framework import serializers
from apps.appointment.models import Appointments
from apps.doctor.models import AppointmentSlot, Doctors


class AppointmentCreateSerializer(serializers.ModelSerializer):
    doctor = serializers.PrimaryKeyRelatedField(
        queryset=Doctors.objects.all(),
        help_text="Doctor ID ni kiriting"
    )
    slot = serializers.PrimaryKeyRelatedField(
        queryset=AppointmentSlot.objects.all(),
        help_text="Slot ID ni kiriting"
    )

    class Meta:
        model = Appointments
        fields = ['doctor', 'slot']

    def validate(self, data):
        doctor = data.get('doctor')
        slot = data.get('slot')

        if slot.doctor != doctor:
            raise serializers.ValidationError(
                {"slot": "Ushbu slot tanlangan doktorga tegishli emas."}
            )
        if not slot.is_available:
            raise serializers.ValidationError(
                {"slot": "Ushbu slot band qilingan."}
            )

        if Appointments.objects.filter(doctor=doctor, slot=slot).exists():
            raise serializers.ValidationError(
                "Bu doktor va slot kombinatsiyasiga allaqachon bemor tayinlangan."
            )

        return data

    def create(self, validated_data):
        patient = self.context['request'].user
        validated_data['patient'] = patient

        slot = validated_data['slot']
        slot.is_available = False
        slot.save()

        return super().create(validated_data)