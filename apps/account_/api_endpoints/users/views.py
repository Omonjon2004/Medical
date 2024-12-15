from rest_framework.viewsets import ModelViewSet

from apps.account_.api_endpoints.users.serializers import UserSerializer
from apps.account_.models import Users
from config.permissions import IsAdminReadOnly


class UsersModelViewSet(ModelViewSet):
    queryset = Users.objects.all()
    serializer_class=UserSerializer
    permission_classes=[IsAdminReadOnly]