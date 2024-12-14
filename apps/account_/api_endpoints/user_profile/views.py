from drf_yasg.utils import swagger_auto_schema
from rest_framework import status

from rest_framework.generics import  ListAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from apps.account_.api_endpoints.user_profile.serializers import (
    UserProfileSerializer, UserProfileUpdateSerializer, )
from apps.account_.models import Users, UserProfile


class ProfileListAPIView(ListAPIView):
    queryset = Users.objects.all().order_by('id')
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=UserProfileUpdateSerializer,
    )
    def user_profile(self, *args, **kwargs):
        user_profile = get_object_or_404(UserProfile, user=self.request.user)
        serializer = UserProfileSerializer(user_profile)
        return Response(serializer.data)


class UserProfileUpdateAPIView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileUpdateSerializer

    @swagger_auto_schema(
        request_body=UserProfileUpdateSerializer,
        responses={200: UserProfileUpdateSerializer}
    )
    def put(self, request):
        user_profile = get_object_or_404(UserProfile, user=self.request.user)
        serializer = self.serializer_class(user_profile, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        request_body=UserProfileUpdateSerializer,
        responses={200: UserProfileUpdateSerializer}
    )
    def patch(self, request):
        user_profile = get_object_or_404(UserProfile, user=self.request.user)
        serializer = self.serializer_class(user_profile, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





