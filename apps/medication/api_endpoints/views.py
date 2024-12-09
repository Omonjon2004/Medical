from django.contrib.postgres.search import TrigramSimilarity
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.medication.models import Medications
from apps.medication.api_endpoints.serializers import MedicationSerializer


class MedicationsRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
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
                queryset.annotate(
                    sim=TrigramSimilarity(
                        'manufacturer', manufacturer))
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


class MedicationAddUpdateView(APIView):
    def post(self, request):
        serializer = MedicationSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data

            medication, created = Medications.objects.update_or_create(
                name=data['name'],
                manufacturer=data['manufacturer'],
                defaults={
                    'description': data.get('description', ''),
                    'dosage_form': data.get('dosage_form', ''),
                    'strength': data.get('strength', ''),
                    'price': data.get('price', 0.0),
                    'stock_quantity': Medications.objects.filter(
                        name=data['name'], manufacturer=data['manufacturer']
                    ).first().stock_quantity + data.get('stock_quantity', 0)
                    if Medications.objects.filter(
                        name=data['name'], manufacturer=data['manufacturer']
                    ).exists() else data.get('stock_quantity', 0),
                }
            )

            if created:
                return Response(
                    {"message": f"Yangi dori yaratildi: {medication.name}"},
                    status=status.HTTP_201_CREATED,
                )
            else:
                return Response(
                    {"message": f"Dori yangilandi: {medication.name}"},
                    status=status.HTTP_200_OK,
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
