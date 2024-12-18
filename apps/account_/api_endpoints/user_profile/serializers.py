from phonenumber_field.serializerfields import PhoneNumberField
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
    full_name = serializers.CharField(
        source='user.full_name',
        required=False,
        read_only=False
    )
    phone_number = PhoneNumberField(
        required=False,
        allow_null=True
    )
    avatar = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = UserProfile
        fields = ['phone_number', 'full_name', 'avatar']
        extra_kwargs = {
            'avatar': {'read_only': False},
        }

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        full_name = user_data.get('full_name')
        if full_name:
            instance.user.full_name = full_name
            instance.user.save()
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance





