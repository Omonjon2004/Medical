from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers

from apps.account_.api_endpoints \
    .change_password.serializers import ChangePasswordSerializer


class ChangePasswordCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def perform_create(self, serializer):
        user = self.request.user
        old_password = serializer.validated_data['old_password']

        if not user.check_password(old_password):
            raise serializers.ValidationError(
                detail={"old_password": "Old password is incorrect."})

        else:
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            raise serializers.ValidationError(
                detail={"new_password": "Successfully changed password."})
