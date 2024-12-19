from datetime import datetime

from rest_framework import serializers
from apps.appointment.models import Appointments
from apps.doctor.models import AppointmentSlot, Doctors


class AppointmentCreateSerializer(serializers.ModelSerializer):
    doctor = serializers.PrimaryKeyRelatedField(
        queryset=Doctors.objects.all(),
        help_text="Doctor ID ni kiriting"
    )
    date = serializers.DateField(help_text="Tayinlash sanasini kiriting (format: YYYY-MM-DD)")
    time = serializers.TimeField(help_text="Tayinlash vaqtini kiriting (format: HH:MM:SS)")

    class Meta:
        model = Appointments
        fields = ['doctor', 'date', 'time']

    def validate(self, data):
        doctor = data.get('doctor')
        date = data.get('date')
        time = data.get('time')
        current_datetime = datetime.now()
        appointment_datetime = datetime.combine(date, time)

        if appointment_datetime <= current_datetime:
            raise serializers.ValidationError(
                "Tayinlash sanasi va vaqti hozirgi vaqtdan keyin bo'lishi kerak."
            )

        # Check if a slot exists for the given doctor, date, and time
        slot = AppointmentSlot.objects.filter(doctor=doctor, date=date, time=time).first()


        # Check if an appointment already exists for the doctor and slot
        if Appointments.objects.filter(doctor=doctor, slot=slot).exists():
            raise serializers.ValidationError(
                "Bu doktor va slot kombinatsiyasiga allaqachon bemor tayinlangan."
            )
        else:
            slot = AppointmentSlot.objects.create(
                doctor=doctor,
                date=date,
                time=time,
                is_available=True
            )

        # Store the slot for later use in the `create` method
        data['slot'] = slot  # Directly assign the slot object

        return data

    def create(self, validated_data):
        patient = self.context['request'].user
        validated_data['patient'] = patient

        slot = validated_data.pop('slot')  # 'slot'ni validated_data'dan chiqaramiz
        slot.is_available = False
        slot.save()

        # Faqat kerakli ma'lumotlarni yuborish:
        appointment = Appointments.objects.create(
            doctor=validated_data['doctor'],
            patient=patient,
            slot=slot,
        )
        return appointment