from django.urls import path

from apps.account.api_endpoints import auth


urlpatterns = [
    path('login/', auth.LoginView.as_view(), name='login'),
    path('register/', auth.RegisterView.as_view(), name='register'),
]