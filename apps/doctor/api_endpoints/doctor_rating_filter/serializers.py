# serializers.py
from rest_framework import serializers

from apps.doctor.models import DoctorRating


class DoctorRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorRating
        fields = ['id', 'doctor', 'rating', 'created_at']
        read_only_fields = ['id', 'created_at']
