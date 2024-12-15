from django.contrib.postgres.search import TrigramSimilarity
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.viewsets import ModelViewSet

from apps.account_.api_endpoints.users.serializers import UserSerializer
from apps.account_.models import Users
from config.permissions import IsAdminReadOnly


class UsersModelViewSet(ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminReadOnly]

    def get_queryset(self):
        queryset = super().get_queryset()
        role = self.request.query_params.get('role')
        full_name=self.request.query_params.get('full_name')
        email=self.request.query_params.get('email')

        if role:
            queryset = (
                queryset.annotate(sim=TrigramSimilarity('role', role))
                .filter(sim__gte=0.2)
                .order_by('-sim')
            )
        if full_name:
            queryset = (
                queryset.annotate(sim=TrigramSimilarity('full_name', full_name))
                .filter(sim__gte=0.2)
                .order_by('-sim')
            )
        if email:
            queryset = (
                queryset.annotate(sim=TrigramSimilarity('email', email))
                .filter(sim__gte=0.2)
                .order_by('-sim')
            )

        return queryset

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "role", openapi.IN_QUERY,
                description="Filter by role",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "full_name", openapi.IN_QUERY,
                description="Filter by full_name",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "email", openapi.IN_QUERY,
                description="Filter by email_name",
                type=openapi.TYPE_STRING,
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
