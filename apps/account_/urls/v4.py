from django.urls import path

from apps.account_.api_endpoints.social_auth import RedirectToGoogleAPIView, callback_google, GoogleLogin

urlpatterns = [
    path('users/google/login/', RedirectToGoogleAPIView.as_view(), name='google-login'),
    path('users/google/callback/', callback_google, name='google-callback'),
    path('users/google/', GoogleLogin.as_view(), name='google-social-login'),
]
