from django.core.cache import cache
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.account_.api_endpoints.activation.verification_code.serializers import VerificationSerializer
from apps.account_.models import Users


class VerificationCodeView(APIView):
    permission_classes = (AllowAny,)

    @swagger_auto_schema(
        request_body=VerificationSerializer
    )
    def post(self, request):
        serializer = VerificationSerializer(data=request.data)
        if serializer.is_valid():
            email = str(serializer.validated_data["email"])
            code = cache.get(email)
            if not code:
                raise ValidationError(
                    detail="Your code has beem expired please try again",
                    code="email")
            else:
                if code == int(serializer.validated_data["code"]):
                    account = get_object_or_404(Users, email=email)
                    account.is_active = True
                    account.save()
                    return Response(
                        data="Your account activated",
                        status=status.HTTP_202_ACCEPTED
                    )
                else:
                    raise ValidationError(
                        detail="Your code is wrong",
                        code="code")
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


__all__ = ("VerificationCodeView",)
