from django.urls import path

from apps.account_.api_endpoints.user_profile import UserProfileUpdateAPIView, UserProfileRetrieveAPIView, \
    UserProfileListAPIView
from apps.account_.api_endpoints.user_profile.views import UserProfileCreateAPIView, UserProfileDeleteAPIView

urlpatterns = [
    path('userprofile-create/',UserProfileCreateAPIView.as_view(),name='userprofile-create'),
    path('userprofile-update/<int:pk>/', UserProfileUpdateAPIView.as_view(), name='userprofile-update'),
    path('userprofile-detail/<int:pk>/',UserProfileRetrieveAPIView.as_view(),name='userprofile-detail'),
    path('userprolife-list/',UserProfileListAPIView.as_view(),name='userprofile-list'),
    path('userprofile-delete/<int:pk>/',UserProfileDeleteAPIView.as_view(),name='userprofile-delete'),
]