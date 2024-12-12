from rest_framework import serializers
from apps.account_.models import Users


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = (
            'id',
            'full_name',
            'role',
            'email',
            'password',
        )
        extra_kwargs = {
            'password': {'write_only': True},
            'role': {'write_only': True},
        }



class ConfirmCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()
    confirm_code = serializers.IntegerField()