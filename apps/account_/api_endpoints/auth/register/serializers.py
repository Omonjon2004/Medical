from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.fields import CharField

from apps.account_.models import Users


class RegistrationSerializer(serializers.ModelSerializer):
    password = CharField(write_only=True)
    confirm_password = CharField(write_only=True)

    class Meta:
        model = Users
        fields = ('id',
                  'full_name',
                  'role',
                  'email',
                  'password',
                  'confirm_password',
                  )
        extra_kwargs = {
            'password': {'read_only': True},
        }

    def validate_email(self, email):
        if Users.objects.filter(email=email).exists():
            raise serializers.ValidationError('Email already registered')
        return email

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise ValidationError(
                detail='Confirm password does not match',
                code='password'
            )
        return attrs

    def create(self, validated_data):
        validated_data['role'] = validated_data.get('role', 'PATIENT')
        account = Users(
            full_name=validated_data['full_name'],
            email=validated_data['email'],
            role=validated_data['role'],
        )
        account.is_active=False
        account.set_password(validated_data['password'])
        account.save()
        return account
