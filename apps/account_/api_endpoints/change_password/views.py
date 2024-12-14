from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from apps.account_.api_endpoints \
    .change_password.serializers import (ChangePasswordSerializer)


class ChangePasswordCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    @swagger_auto_schema(

        request_body=ChangePasswordSerializer,
    )
    def change_password(self, request, *args, **kwargs):
        serializer = ChangePasswordSerializer(
            data=request.data,
            context={'request': request}
        )

        if serializer.is_valid(raise_exception=True):
            user = request.user
            user.set_password(
                serializer.validated_data['new_password']
            )
            user.save()
            return Response(
                data={"detail": "your password has been successfully changed"},
                status=status.HTTP_200_OK
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


__all__ = ['ChangePasswordCreateAPIView']
