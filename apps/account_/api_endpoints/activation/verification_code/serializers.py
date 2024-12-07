from rest_framework.exceptions import ValidationError
from rest_framework.fields import CharField, EmailField
from rest_framework.serializers import Serializer

from apps.account_.models import Users


class VerificationSerializer(Serializer):
    email = EmailField()
    code = CharField()

    def validate_code(self, code):
        if len(code) != 4:
            raise ValidationError(detail="Code lenght must be 4", code="code")
        return code

    def validate_email(self, email):
        if not Users.objects.filter(email=email).exists():
            raise ValidationError(
                detail=f"with {email} user not found",
                code="email")
        return email
