from django.contrib.postgres.search import TrigramSimilarity
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from apps.medication.models import Medications
from apps.medication.api_endpoints.serializers import MedicationSerializer


class MedicationsRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = MedicationSerializer
    queryset = Medications.objects.all()
    permission_classes = (IsAuthenticated,)


class MedicationsCreateAPIView(CreateAPIView):
    serializer_class = MedicationSerializer
    queryset = Medications.objects.all()
    permission_classes = (IsAuthenticated,)


class MedicationListAPIView(ListAPIView):
    serializer_class = MedicationSerializer
    queryset = Medications.objects.all()
    permission_classes = (IsAuthenticated,)
    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.query_params.get('name')
        manufacturer = self.request.query_params.get('manufacturer')

        if name:
            queryset = (
                queryset.annotate(sim=TrigramSimilarity('name', name))
                .filter(sim__gte=0.2)
                .order_by('-sim')
            )
        if manufacturer:
            queryset = (
                queryset.annotate(sim=TrigramSimilarity('manufacturer', manufacturer))
                .filter(sim__gte=0.2)
                .order_by('-sim')
            )
        return queryset

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "name", openapi.IN_QUERY,
                description="Filter by name",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                "manufacturer", openapi.IN_QUERY,
                description="Filter by manufacturer",
                type=openapi.TYPE_STRING
            ),
        ]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
