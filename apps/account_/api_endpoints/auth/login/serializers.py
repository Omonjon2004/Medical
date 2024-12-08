from django.contrib.auth import authenticate
from rest_framework.exceptions import ValidationError
from rest_framework.fields import CharField, EmailField
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from apps.account_.models import Users


class LoginSerializer(TokenObtainPairSerializer):
    email = EmailField()
    password = CharField()

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")
        try:
            user = Users.objects.get(email=email)
        except Users.DoesNotExist:
            raise ValidationError({"error": "User not found"})

        if not user.is_active:
            raise ValidationError({"error": "This account is inactive"})

        user = authenticate(username=email, password=password)
        if not user:
            raise ValidationError({"error": "Password is incorrect"})

        return super().validate(attrs)

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        return token
