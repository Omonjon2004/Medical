# from allauth.socialaccount.providers.apple.views import (
#     AppleOAuth2Adapter)
# from allauth.socialaccount.providers.facebook.views import (
#     FacebookOAuth2Adapter)
# from allauth.socialaccount.providers.google.views import (
#     GoogleOAuth2Adapter)
# from allauth.socialaccount.providers.oauth2.client import (
#     OAuth2Client)
#
# from dj_rest_auth.registration.views import SocialLoginView
#
#
# class FacebookLogin(SocialLoginView):
#     adapter_class = FacebookOAuth2Adapter
#
#
# class GoogleLogin(SocialLoginView):
#     adapter_class = GoogleOAuth2Adapter
#     callback_url = "http://127.0.0.1:8000/accounts/google/login/callback/"
#     client_class = OAuth2Client
#
#
# class AppleLogin(SocialLoginView):
#     adapter_class = AppleOAuth2Adapter
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


class GoogleCallbackView(APIView):
    permission_classes = (AllowAny,)
    @swagger_auto_schema(
        operation_summary="Google Login Callback",
        operation_description="This endpoint is the callback for Google OAuth login. It's automatically handled by Django Allauth.",
        responses={200: "Login successful, user redirected."},
    )
    def get(self, request):
        return Response(status=200)