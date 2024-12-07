from rest_framework.decorators import action
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from apps.account_.api_endpoints.user_profile.serializers import UserProfileSerializer
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

    @action(methods=["put", "patch"], detail=False)
    def update_profile(self, request, *args, **kwargs):
        # Foydalanuvchining profilini oling
        user_profile = get_object_or_404(UserProfile, user=request.user)

        # Ma'lumotlarni yangilang
        serializer = UserProfileSerializer(user_profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        account = get_object_or_404(Users, pk=self.request.user.id)
        self.perform_destroy(account)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()

    # @action(methods=["post"], detail=False)
    # def account_exit(self, *args, **kwargs):
    #     account = get_object_or_404(Users, pk=self.request.user.id)
    #     account.is_active = False
    #     account.save()
    #     return Response(status=status.HTTP_200_OK)
