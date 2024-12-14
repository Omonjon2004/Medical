from rest_framework import serializers
from apps.account_.models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    role = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = (
            'id',
            'full_name',
            'email',
            'role',
            'phone_number',
            'avatar',
            'user',
            'created_at',
            'updated_at',
        )

        extra_kwargs = {
            'id': {'read_only': True},
            'role': {'read_only': True},
            'email': {'read_only': True},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},

        }

    def get_full_name(self, obj):
        return obj.user.full_name

    def get_email(self, obj):
        return obj.user.email

    def get_role(self, obj):
        return obj.user.role


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = (
            'id',
            'full_name',
            'phone_number',
            'avatar',
        )
        extra_kwargs = {
            'id': {'read_only': True},
            'phone_number': {'required': False},
            'avatar': {'required': False},
        }

    def get_full_name(self, obj):
        return obj.user.full_name

