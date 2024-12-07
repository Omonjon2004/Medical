from django.urls import path, include
from rest_framework.routers import DefaultRouter
router = DefaultRouter()

from apps.account_.api_endpoints.user_profile import ProfileViewSet

router.register(r'profile', ProfileViewSet, basename='profile')

urlpatterns = [
    path('', include(router.urls)),

]