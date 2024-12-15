from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import ListAPIView, UpdateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView

from apps.account_.api_endpoints.user_profile.serializers import (
    UserProfileSerializer, UserProfileUpdateSerializer, )
from apps.account_.models import Users, UserProfile


class ProfileListAPIView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer

    def get_object(self):
        return get_object_or_404(UserProfile, user=self.request.user)

    def get(self, request, *args, **kwargs):
        user_profile = self.get_object()
        serializer = self.get_serializer(user_profile)
        return Response(serializer.data)


class UserProfileUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileUpdateSerializer

    def get_object(self):
        return self.request.user

    @swagger_auto_schema(
        request_body=UserProfileUpdateSerializer,
    )
    def put(self, request, *args, **kwargs):
        user_profile = self.get_object()
        serializer = self.serializer_class(user_profile, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
     request_body=UserProfileUpdateSerializer,
    )
    def patch(self, request, *args, **kwargs):
        user_profile = self.get_object()
        serializer = self.serializer_class(user_profile, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
