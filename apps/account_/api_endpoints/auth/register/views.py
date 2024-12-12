import json
import random
from django.core.cache import cache
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import CreateAPIView, GenericAPIView

from apps.account_.api_endpoints.auth.register.serializers import ConfirmCodeSerializer, RegistrationSerializer
from apps.account_.models import Users
from apps.account_.tasks import send_email


class RegistrationAPIView(CreateAPIView):
    serializer_class = RegistrationSerializer
    permission_classes = [AllowAny]

    def generate_confirmation_code(self):
        return random.randrange(100000, 999999)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        full_name = serializer.validated_data['full_name']
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        role = serializer.validated_data['role']
        confirm_code = self.generate_confirmation_code()
        print(confirm_code)

        cache_key = f"user_cache_{email}"
        cache_data = {
            'full_name': full_name,
            'password': password,
            'role': role,
            'confirmation_code': confirm_code,
        }

        cache.set(cache_key, json.dumps(cache_data), timeout=300)

        send_email.delay(email, confirm_code)
        return Response({'message': 'Confirmation code sent!'}, status=status.HTTP_201_CREATED)


class ConfirmCodeApiView(GenericAPIView):
    serializer_class = ConfirmCodeSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        confirm_code = request.data.get('confirm_code')


        cache_key = f"user_cache_{email}"


        cached_data = cache.get(cache_key)
        if cached_data:
            cached_data = json.loads(cached_data)


        if cached_data and str(confirm_code) == str(cached_data.get('confirmation_code')):
            full_name = cached_data.get('full_name')
            password = cached_data.get('password')
            role = cached_data.get('role')

            if Users.objects.filter(email=email).exists():
                return Response({'message': 'Email already registered!'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                user = Users(
                    email=email,
                    full_name=full_name,
                    role=role
                )
                user.set_password(password)
                user.save()
                return Response({'message': 'Email registered!'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': 'Confirmation code does not match or expired!'},
                            status=status.HTTP_400_BAD_REQUEST)
