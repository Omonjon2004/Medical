from rest_framework import serializers
from apps.doctor.models import AppointmentSlot, Doctors
from datetime import date

class AppointmentSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppointmentSlot
        fields = ('time', 'is_available')

class DoctorDetailSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    available_slots = serializers.SerializerMethodField()

    class Meta:
        model = Doctors
        fields = (
            'id',
            'full_name',
            'specialization',
            'ratings',
            'bio',
            'available_slots'
        )

    def get_full_name(self, obj):
        return f"{obj.user.full_name}"

    def get_available_slots(self, obj):
        date_str = self.context.get('date')  # Get the date parameter from the request context
        if date_str:
            try:
                selected_date = date.fromisoformat(date_str)
                slots = AppointmentSlot.objects.filter(doctor=obj, date=selected_date)

                if slots.exists():
                    return AppointmentSlotSerializer(slots, many=True).data
                else:
                    return {'message': 'Doctor is not working on this day.'}
            except ValueError:
                return {'error': 'Invalid date format.'}
        else:
            return {'error': 'Date parameter is required.'}
