from django.db import transaction
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.generics import RetrieveAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404


from apps.account_.api_endpoints.user_profile.serializers import (
    UserProfileSerializer, UserProfileUpdateSerializer, )
from apps.account_.models import UserProfile


class ProfileListAPIView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer

    def get_object(self):
        return get_object_or_404(UserProfile,
                                 user=self.request.user)

    def get(self, request, *args, **kwargs):
        user_profile = self.get_object()
        serializer = self.get_serializer(user_profile)
        return Response(serializer.data)


from rest_framework_simplejwt.token_blacklist.models import OutstandingToken
from django.db import transaction
from rest_framework.response import Response
from rest_framework import status

class UserProfileUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileUpdateSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['patch', 'put', 'delete']
    parser_classes = [MultiPartParser, FormParser]

    def get_object(self):
        return self.request.user.profile

    def perform_destroy(self, instance):
        user = instance.user
        with transaction.atomic():
            OutstandingToken.objects.filter(user=user).delete()
            instance.delete()
            user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
