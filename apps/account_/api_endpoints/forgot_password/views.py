import random

from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.account_.api_endpoints.forgot_password.serializers import (
    ForgotPasswordSerializers)
from apps.account_.models import Users
from apps.account_.tasks import send_forgot_password_code


import secrets
from django.shortcuts import get_object_or_404


class ForgotPasswordAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = ForgotPasswordSerializers

    @swagger_auto_schema(request_body=ForgotPasswordSerializers)
    def post(self, request):
        serializer = ForgotPasswordSerializers(data=request.data)
        if serializer.is_valid():
            new_password =str( secrets.randbelow(900000) + 100000)
            user = get_object_or_404(Users, email=serializer.validated_data['email'])
            user.set_password(new_password)
            user.save()

            send_forgot_password_code.delay(
                email=user.email,
                subject="Reset Your Password",
                new_password=new_password
            )

            return Response({"detail": "A new password has been sent."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




