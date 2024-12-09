from rest_framework import serializers

from apps.patient.models import Patients


class PatientCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patients
        fields = (
            'id',
            'user_id',
            'age',
            'gender',
            'medical_history',
            'additional_phone_number',
            'created_at',
            'updated_at',
        )
        extra_kwargs = {
            'id': {'read_only': True},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
        }

        def get_full_name(self, obj):
            return obj.user_id.full_name


class PatientUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patients
        fields = (
            'id',
            'age',
            'gender',
            'medical_history',
            'additional_phone_number',
            'created_at',
            'updated_at',
        )
        extra_kwargs = {
            'id': {'read_only': True},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
        }


class PatientDetailSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = Patients
        fields = (
            'id',
            'full_name',
            'age',
            'gender',
            'medical_history',
            'additional_phone_number',
            'created_at',
            'updated_at',
        )
        extra_kwargs = {
            'id': {'read_only': True},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
        }

    def get_full_name(self, obj):
        return obj.user_id.full_name


class PatientListSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = Patients
        fields = (
            'id',
            'full_name',
            'age',
            'gender',
            'medical_history',
            'additional_phone_number',
            'created_at',
            'updated_at',
        )

    def get_full_name(self, obj):
        return obj.user_id.full_name
