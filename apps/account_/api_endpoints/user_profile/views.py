from rest_framework import generics
from rest_framework.exceptions import NotAuthenticated, PermissionDenied
from rest_framework.permissions import IsAuthenticated
from apps.account_.api_endpoints.user_profile.serializers import (
    UserProfileCreateSerializer,
    UserProfileUpdateSerializer,
    UserProfileDetailsSerializer,
)
from apps.account_.models import UserProfile


class UserProfileCreateAPIView(generics.CreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UserProfileUpdateAPIView(generics.UpdateAPIView):
    serializer_class = UserProfileUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        if getattr(self, 'swagger_fake_view', False):
            return UserProfile.objects.none()


        if not self.request.user.is_authenticated:
            raise NotAuthenticated("The user is not authenticated.")


        return UserProfile.objects.filter(user=self.request.user)


class UserProfileRetrieveAPIView(generics.RetrieveAPIView):

    serializer_class = UserProfileDetailsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserProfile.objects.filter(user=self.request.user)


class UserProfileListAPIView(generics.ListAPIView):
    serializer_class = UserProfileDetailsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role == 'ADMIN':
            return UserProfile.objects.all()

        raise PermissionDenied("You do not have access to this information")


class UserProfileDeleteAPIView(generics.DestroyAPIView):
    serializer_class = UserProfileDetailsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserProfile.objects.filter(user=self.request.user)
