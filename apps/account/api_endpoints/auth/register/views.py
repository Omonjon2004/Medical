from rest_framework import generics

from apps.account.api_endpoints.auth.register.serializers import RegistrationSerializer
from apps.account.models import Users


class RegisterView(generics.CreateAPIView):
    queryset = Users.objects.all()
    serializer_class = RegistrationSerializer


__all__ = ['RegisterView', ]
