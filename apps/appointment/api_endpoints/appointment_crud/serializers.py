from rest_framework import serializers

from apps.appointment.models import Appointments
from apps.doctor.models import Doctors, AppointmentSlot


class DoctorSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = Doctors
        fields = ['id', 'full_name', 'specialization']  # doctor modelidagi maydonlar

    def get_full_name(self, obj):
        return obj.user.full_name

class SlotSerializer(serializers.ModelSerializer):
    date = serializers.SerializerMethodField()

    class Meta:
        model = AppointmentSlot
        fields = ['id', 'date', 'time']  # Slot uchun kerakli maydonlar

    def get_date(self, obj):
        return obj.date.strftime("%Y-%m-%d")  # Yil-Kun-Oy va Vaqt formatida


class AppointmentSerializer(serializers.ModelSerializer):
    doctor = DoctorSerializer()  # Nested serializer orqali doctor ma'lumotlari
    slot = SlotSerializer()  # Slot ma'lumotlarini chiqarish

    class Meta:
        model = Appointments
        fields = ['id', 'doctor', 'slot', 'status']