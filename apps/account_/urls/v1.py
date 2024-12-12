from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from apps.account_.api_endpoints.auth import RegistrationAPIView, ConfirmCodeApiView, LoginView
from apps.account_.api_endpoints.auth.logout import LogoutView
from apps.account_.api_endpoints.forgot_password import ForgotPasswordAPIView

urlpatterns = [
    path('api/user/register/', RegistrationAPIView.as_view(), name='register'),
    path('api/user/confirm-code/', ConfirmCodeApiView.as_view(), name='confirm-code'),
    path('api/user/login/', LoginView.as_view(), name='login'),
    path('api/user/token-refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/user/logout/', LogoutView.as_view(), name='logout'),
    path('api/user/forgot_password/', ForgotPasswordAPIView.as_view(), name='forgot_password')
]
