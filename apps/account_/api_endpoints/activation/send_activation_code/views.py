from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.account_.api_endpoints.activation.send_activation_code.serializers import SendActivationCodeSerializer
from apps.account_.tasks import send_email_code


class SendActivationCodeAPIView(APIView):
    permission_classes = [AllowAny, ]

    @swagger_auto_schema(
        request_body=SendActivationCodeSerializer
    )
    def post(self, request):
        serializer = SendActivationCodeSerializer(data=request.data)

        if serializer.is_valid():
            send_email_code.delay(
                email=request.data['email'],
                subject="Welcome to Medical center.")

            return Response("activation code has been sent",
                            status.HTTP_200_OK)

        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


__all__ = ("SendActivationCodeAPIView",)
