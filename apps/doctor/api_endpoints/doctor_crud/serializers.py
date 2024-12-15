from rest_framework import serializers
from apps.doctor.models import Doctors


class DoctorCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctors
        fields = (
            'specialization',
            'experience_years',
            'ratings',
            'bio',
            'created_at',
            'updated_at',
        )
        extra_kwargs = {
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
            'user': {'read_only': True},
        }

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user

        doctor = Doctors.objects.create(**validated_data)
        return doctor


class DoctorUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctors
        fields = (
            'user',
            'specialization',
            'experience_years',
            'ratings',
            'bio',
            'created_at',
            'updated_at',
        )
        extra_kwargs = {
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
            'user': {'read_only': True},
            'ratings': {'read_only': True},
        }


class DoctorListSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = Doctors
        fields = (
            'id',
            'full_name',
            'specialization',
            'experience_years',
            'ratings',
            'bio'
        )

    def get_full_name(self, obj):
        return obj.user.full_name


class DoctorDetailSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = Doctors
        fields = (

            'id',
            'full_name',
            'specialization',
            'bio'
        )
        extra_kwargs = {
            'full_name': {'read_only': True},
            'bio': {'read_only': True},
            'specialization': {'read_only': True},
        }

    def get_full_name(self, obj):
        return obj.user.full_name
