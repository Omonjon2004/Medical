from rest_framework import serializers

from apps.appointment.models import Appointments
from apps.doctor.models import AppointmentSlot, Doctors


class AppointmentSerializer(serializers.ModelSerializer):
    doctor = serializers.PrimaryKeyRelatedField(
        queryset=Doctors.objects.all()
    )
    slot = serializers.PrimaryKeyRelatedField(
        queryset=AppointmentSlot.objects.all()
    )

    class Meta:
        model = Appointments
        fields = [
            'id',
            'doctor',
            'slot',
            'patient',
            'status',
            'confirmed',
            'created_at'
        ]

    def create(self, validated_data):
        patient = self.context['request'].user

        doctor = validated_data.get('doctor')
        slot = validated_data.get('slot')

        if not doctor or not slot:
            raise serializers.ValidationError(
                "Doctor va slot ma'lumotlari kiritilishi kerak."
            )

        existing_appointment = Appointments.objects.filter(
            doctor=doctor, slot=slot
        ).first()
        if existing_appointment:
            raise serializers.ValidationError(
                "Bu doktor va slot kombinatsiyasiga "
                "allaqachon bemor tayinlangan."
            )

        validated_data['patient'] = patient
        return super().create(validated_data)
