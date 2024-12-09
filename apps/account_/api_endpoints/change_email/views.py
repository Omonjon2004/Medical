from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from apps.account_.api_endpoints \
    .change_email.serializers import ChangeEmailSerializer


class ChangeEmailViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    @action(methods=['post'], detail=False)
    def update_email(self, request, *args, **kwargs):
        serializer = ChangeEmailSerializer(
            data=request.data,
            context={'request': request})
        if serializer.is_valid(
                raise_exception=True):
            user = request.user
            user.email = serializer.validated_data['new_email']
            user.is_active = False
            user.save()
            return Response(
                {"detail": "Email changed successfully."},
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
