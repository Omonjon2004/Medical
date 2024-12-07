from rest_framework.exceptions import ValidationError
from rest_framework.fields import EmailField
from rest_framework.serializers import Serializer

from apps.account_.models import Users


class SendActivationCodeSerializer(Serializer):
    email = EmailField()

    def validate_email(self, email):
        if not Users.objects.filter(email=email).exists():
            raise ValidationError(
                detail=f"with {email} user not found",
                code="email")

        return email
