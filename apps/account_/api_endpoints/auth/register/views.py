from rest_framework import generics, permissions

from apps.account_.api_endpoints.auth.register.serializers import (
    RegistrationSerializer)
from apps.account_.models import Users


class RegisterView(generics.CreateAPIView):
    queryset = Users.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = (permissions.AllowAny,)


__all__ = ['RegisterView', ]
