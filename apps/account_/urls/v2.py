from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.account_.api_endpoints.change_email.views import ChangeEmailViewSet
from apps.account_.api_endpoints.change_password import ChangePasswordViewSet

router = DefaultRouter()

from apps.account_.api_endpoints.user_profile import ProfileViewSet

router.register(r'profile', ProfileViewSet, basename='profile')
router.register(r'user-change-password', ChangePasswordViewSet, basename='change-password')
router.register(r'user-change-email', ChangeEmailViewSet, basename='change-email')
urlpatterns = [
    path('', include(router.urls)),
]
