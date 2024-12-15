from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from apps.account_.api_endpoints \
    .change_email.serializers import ChangeEmailSerializer


class ChangeEmailCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChangeEmailSerializer

    def post(self, request, *args, **kwargs):
        serializer = ChangeEmailSerializer(
            data=request.data,
            context={'request': request})
        if serializer.is_valid(
                raise_exception=True):
            user = request.user
            user.email = serializer.validated_data['new_email']
            user.save()
            return Response(
                {"detail": "Email changed successfully."},
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
