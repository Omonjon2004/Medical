from django.urls import path

from apps.account_.api_endpoints.activation import VerificationCodeView, SendActivationCodeAPIView
from apps.account_.api_endpoints.forgot_password import ForgotPasswordAPIView

urlpatterns = [
    path('account-verification-code/', VerificationCodeView.as_view(), name='account_verification_code'),
    path('send-activation-code/', SendActivationCodeAPIView.as_view(), name='send_activation_code'),
    path('forgot_password/', ForgotPasswordAPIView.as_view(), name='forgot_password')

]
