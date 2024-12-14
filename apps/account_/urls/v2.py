from django.urls import path

from apps.account_.api_endpoints.change_email.views import ChangeEmailCreateAPIView
from apps.account_.api_endpoints.change_password import ChangePasswordCreateAPIView



from apps.account_.api_endpoints.user_profile import ProfileListAPIView, UserProfileUpdateAPIView


urlpatterns = [
    path('user/profile-user/', ProfileListAPIView.as_view(), name='user-profile'),
    path('user/change-password/',ChangePasswordCreateAPIView.as_view(),name='change_password'),
    path('user/change-email/',ChangeEmailCreateAPIView.as_view(),name='change_email'),
    path('user/update-user/', UserProfileUpdateAPIView.as_view(), name='update_user_profile'),
]
