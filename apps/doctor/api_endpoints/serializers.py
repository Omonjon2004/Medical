from rest_framework import serializers
from apps.doctor.models import Doctors


class DoctorCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctors
        fields = (
            'user_id',
            'specialization',
            'experience_years',
            'available_times',
            'ratings',
            'bio',
            'created_at',
            'updated_at',
        )
        extra_kwargs = {
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
        }


class DoctorUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctors
        fields = (
            'user_id',
            'specialization',
            'experience_years',
            'available_times',
            'ratings',
            'bio',
            'created_at',
            'updated_at',
        )
        extra_kwargs = {
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
            'user_id': {'read_only': True},
            'ratings': {'read_only': True},
        }


class DoctorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctors
        fields = (
            'id',
            'specialization',
            'experience_years',
            'available_times',
            'ratings',
            'bio'
        )
