from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from apps.account_.api_endpoints.user_profile.serializers import (
    UserProfileSerializer)
from apps.account_.models import Users, UserProfile


class ProfileViewSet(viewsets.ViewSet):
    queryset = Users.objects.all().order_by('id')
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    @action(methods=["get"], detail=False)
    def user_profile(self, *args, **kwargs):
        user_profile = get_object_or_404(UserProfile, user=self.request.user)
        serializer = UserProfileSerializer(user_profile)
        return Response(serializer.data)

# class User

