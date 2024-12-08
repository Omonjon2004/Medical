from django.contrib.postgres.search import TrigramSimilarity
from django.db.models import CharField
from django.db.models.functions import Cast
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny

from apps.doctor.api_endpoints.doctor_search.serializers import DoctorSearchSerializer
from apps.doctor.models import Doctors


class DoctorSearchAPIView(ListAPIView):
    serializer_class = DoctorSearchSerializer
    queryset = Doctors.objects.all()
    permission_classes = (AllowAny,)

    def get_queryset(self):
        queryset = super().get_queryset()
        full_name = self.request.query_params.get('full_name')
        specialization = self.request.query_params.get('specialization')

        # TrigramSimilarity bilan annotatsiya
        if full_name:
            queryset = (
                queryset.annotate(
                    sim=TrigramSimilarity(
                        Cast('user_id__full_name', CharField()), full_name
                    )
                )
                .filter(sim__gte=0.2)
                .order_by('-sim')
            )
        if specialization:
            queryset = (
                queryset.annotate(sim=TrigramSimilarity('specialization', specialization))
                .filter(sim__gte=0.2)
                .order_by('-sim')
            )
        return queryset

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "full_name", openapi.IN_QUERY,
                description="Filter by doctor's full name",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "specialization", openapi.IN_QUERY,
                description="Filter by doctor's specialization",
                type=openapi.TYPE_STRING,
            ),
        ]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
