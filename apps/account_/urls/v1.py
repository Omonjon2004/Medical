from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from apps.account_.api_endpoints import auth
from apps.account_.api_endpoints.auth.logout import LogoutView
from apps.account_.api_endpoints.social_auth import GoogleCallbackView

# from apps.account_.api_endpoints.social_auth import FacebookLogin, GoogleLogin, AppleLogin

urlpatterns = [
    path('login/', auth.LoginView.as_view(), name='login'),
    path('register/', auth.RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('accounts/google/login/callback/', GoogleCallbackView.as_view(), name='google-callback'),

    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
