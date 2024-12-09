from rest_framework_simplejwt.views import TokenViewBase

from apps.account_.api_endpoints.auth.login.serializers import LoginSerializer


class LoginView(TokenViewBase):
    serializer_class = LoginSerializer


__all__ = ("LoginView",)
