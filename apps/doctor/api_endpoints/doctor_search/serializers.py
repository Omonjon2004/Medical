from rest_framework import serializers
from apps.doctor.models import Doctors

class DoctorSearchSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='user_id.full_name', read_only=True)

    class Meta:
        model = Doctors
        fields = ['id', 'full_name', 'specialization', 'ratings']
