from rest_framework.exceptions import ValidationError
from rest_framework.fields import EmailField
from rest_framework.serializers import Serializer

from apps.account_.models import Users


class ForgotPasswordSerializers(Serializer):
    email = EmailField()

    def validate_email(self, email):
        try:
            user = Users.objects.get(email=email)
        except Users.DoesNotExist:
            raise ValidationError(
                detail=f"User with email {email} not found.",
                code="email"
            )
        if not user.is_active:
            raise ValidationError(
                detail=f"""
                User with email {email} does not have an active account.""",
                code="email"
            )
        return email
