from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.account_.api_endpoints.users import UsersModelViewSet

router = DefaultRouter()
router.register("", UsersModelViewSet)

urlpatterns = [
    path('',include(router.urls)),
]