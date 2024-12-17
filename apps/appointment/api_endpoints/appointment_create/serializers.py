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

class AppointmentRescheduleSerializer(serializers.ModelSerializer):
    new_slot = serializers.PrimaryKeyRelatedField(
        queryset=AppointmentSlot.objects.all(),
        help_text="Yangi slot ID ni kiriting"
    )

    class Meta:
        model = Appointments
        fields = ['new_slot']

    def validate(self, data):
        appointment = self.instance  # Hozirgi tayinlash
        new_slot = data.get('new_slot')

        # Yangi slot eski doktorga tegishli ekanligini tekshirish
        if new_slot.doctor != appointment.doctor:
            raise serializers.ValidationError(
                {"new_slot": "Yangi slot tanlangan doktorga tegishli emas."}
            )

        # Slot band emasligini tekshirish
        if not new_slot.is_available:
            raise serializers.ValidationError(
                {"new_slot": "Yangi slot allaqachon band qilingan."}
            )
        return data

    def update(self, instance, validated_data):
        # Eski slotni 'is_available' holatiga qaytarish
        old_slot = instance.slot
        old_slot.is_available = True
        old_slot.save()

        # Yangi slotni band qilish
        new_slot = validated_data['new_slot']
        new_slot.is_available = False
        new_slot.save()

        # Tayinlashdagi slotni yangilash
        instance.slot = new_slot
        instance.save()
        return instance