from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from apps.account_.api_endpoints import auth
from apps.account_.api_endpoints.auth.logout import LogoutView
from apps.account_.api_endpoints.social_auth import FacebookLogin, GoogleLogin, AppleLogin

urlpatterns = [
    path('login/', auth.LoginView.as_view(), name='login'),
    path('register/', auth.RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('facebook/', FacebookLogin.as_view(), name='fb_login'),
    path('google/', GoogleLogin.as_view(), name='google_login'),
    path('apple/login/', AppleLogin.as_view(), name='apple-login'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

