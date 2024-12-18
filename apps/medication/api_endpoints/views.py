from django.contrib.postgres.search import TrigramSimilarity
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.medication.models import Medications
from apps.medication.api_endpoints.serializers import MedicationSerializer, MedicationRatingSerializer
from config.permissions import IsAdminReadOnly


class MedicationUpdateAPIView(APIView):
    permission_classes = (IsAdminReadOnly,)
    serializer_class = MedicationSerializer

    @swagger_auto_schema(
        request_body=MedicationSerializer,
        responses={status.HTTP_200_OK: MedicationSerializer}
    )
    def put(self, request, pk):
        try:
            medication = Medications.objects.get(pk=pk)
        except Medications.DoesNotExist:
            return Response(
                data={"error": "Medication not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = MedicationSerializer(medication,
                                          data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,
                            status=status.HTTP_200_OK)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        request_body=MedicationSerializer,
        responses={status.HTTP_200_OK: MedicationSerializer}
    )
    def patch(self, request, pk):
        try:
            medication = Medications.objects.get(pk=pk)
        except Medications.DoesNotExist:
            return Response(
                data={"error": "Medication not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = MedicationSerializer(
            medication,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,
                            status=status.HTTP_200_OK)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        responses={status.HTTP_200_OK: MedicationSerializer}
    )
    def get(self, request, pk):
        try:
            medication = Medications.objects.get(pk=pk)
        except Medications.DoesNotExist:
            return Response(
                data={"error": "Medication not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = MedicationSerializer(medication)
        return Response(serializer.data,
                        status=status.HTTP_200_OK)

    @swagger_auto_schema(
        responses={status.HTTP_204_NO_CONTENT: "Deleted successfully"}
    )
    def delete(self, request, pk):
        try:
            medication = Medications.objects.get(pk=pk)
            medication.delete()
            return Response(
                data={"message": "Medication deleted successfully"},
                status=status.HTTP_204_NO_CONTENT
            )
        except Medications.DoesNotExist:
            return Response(
                data={"error": "Medication not found"},
                status=status.HTTP_404_NOT_FOUND
            )


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


class MedicationCreateAPIView(APIView):
    serializer_class = MedicationSerializer
    queryset = Medications.objects.all()
    permission_classes = (IsAdminUser,)

    @swagger_auto_schema(
        request_body=MedicationSerializer,
    )
    def post(self, request):
        serializer = MedicationSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data

            existing_medication = Medications.objects.filter(
                name=data['name'],
                manufacturer=data['manufacturer']
            ).first()

            if existing_medication:
                new_stock_quantity = (existing_medication.stock_quantity
                                      + data.get('stock_quantity', 0))
                medication = Medications.objects.update_or_create(
                    name=data['name'],
                    manufacturer=data['manufacturer'],
                    defaults={
                        'description': data.get('description', ''),
                        'dosage_form': data.get('dosage_form', ''),
                        'strength': data.get('strength', ''),
                        'price': data.get('price', 0.0),
                        'stock_quantity': new_stock_quantity
                    }
                )
                return Response(
                    data={
                        "message": f"Medicine updated: {medication[0].name}"},
                    status=status.HTTP_200_OK,
                )
            else:
                medication = Medications.objects.create(
                    name=data['name'],
                    manufacturer=data['manufacturer'],
                    description=data.get('description', ''),
                    dosage_form=data.get('dosage_form', ''),
                    strength=data.get('strength', ''),
                    price=data.get('price', 0.0),
                    stock_quantity=data.get('stock_quantity', 0),
                )
                return Response(
                    data={"message": f"Medicine created: {medication.name}"},
                    status=status.HTTP_201_CREATED,
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MedicationRatingAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=MedicationRatingSerializer,
    )

    def post(self, request):
        serializer = MedicationRatingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
