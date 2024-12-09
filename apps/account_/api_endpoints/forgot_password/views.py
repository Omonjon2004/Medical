from django.utils.crypto import get_random_string
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.account_.api_endpoints.forgot_password.serializers import (
    ForgotPasswordSerializers)
from apps.account_.models import Users
from apps.account_.tasks import send_forgot_password_code


class ForgotPasswordAPIView(APIView):
    permission_classes = [AllowAny, ]

    @swagger_auto_schema(
        request_body=ForgotPasswordSerializers
    )
    def post(self, request):
        serializer = ForgotPasswordSerializers(data=request.data)
        if serializer.is_valid():

            new_password = get_random_string(length=8)
            user = Users.objects.get(
                email=serializer.validated_data['email'])
            user.set_password(new_password)
            user.save()

            send_forgot_password_code.delay(
                email=request.data['email'],
                subject="Please change your password "
                        "after logging in for security reasons",
                new_password=new_password
            )

            return Response("New password has been sent", status.HTTP_200_OK)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


__all__ = ("ForgotPasswordAPIView",)
