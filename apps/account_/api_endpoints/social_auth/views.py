from django.shortcuts import redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
import os
import requests
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView
from dotenv import load_dotenv
load_dotenv()


# Google OAuth2 Login Redirect
class RedirectToGoogleAPIView(APIView):

    def get(self, request):
        google_redirect_uri = os.getenv('GOOGLE_REDIRECT_UTI')
        google_client_id = os.getenv('GOOGLE_CLIENT_ID')

        url = (
            f'https://accounts.google.com/o/oauth2/v2/auth?'
            f'redirect_uri={google_redirect_uri}&'
            f'prompt=consent&'
            f'response_type=code&'
            f'client_id={google_client_id}&'
            f'scope=openid email profile&'
            f'access_type=offline'
        )
        print('Redirect URL: -->', url)
        return redirect(url)


# Google OAuth2 Login Callback
class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = os.getenv('CALLBACK_URL')
    client_class = OAuth2Client


@api_view(["GET"])
def callback_google(request):
    code = request.GET.get("code")
    if not code:
        return Response({"success": False, "message": "Authorization code not provided"}, status=400)

    google_token_endpoint = os.getenv('GOOGLE_TOKEN_ENDPOINT')
    payload = {
        "code": code,
        "client_id": os.getenv('GOOGLE_CLIENT_ID'),
        "client_secret": os.getenv('GOOGLE_CLIENT_SECRET'),
        "redirect_uri":os.getenv('GOOGLE_REDIRECT_UTI'),
        "grant_type": "authorization_code",
    }

    try:
        response = requests.post(google_token_endpoint, data=payload, timeout=30)
        response.raise_for_status()
        return Response(response.json())
    except requests.RequestException as e:
        return Response({"success": False, "error": str(e)}, status=500)
