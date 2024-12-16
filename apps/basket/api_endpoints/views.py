from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet

from apps.basket.api_endpoints.serializers import \
    BasketDetailSerializer, BasketCreateSerializer, BasketItemSerializer, BasketItemAdminSerializer
from apps.basket.models import Basket, BasketItem
from apps.medication.models import Medications
from config.permissions import IsAdminReadOnly


class AddToBasketView(APIView):
    @swagger_auto_schema(
        request_body=BasketCreateSerializer,
    )
    def post(self, request, *args, **kwargs):
        serializer = BasketCreateSerializer(data=request.data)
        if serializer.is_valid():
            medications_data = serializer.validated_data['medications']
            user = request.user

            basket = Basket.objects.create(user=user)

            response_data = []
            total_price = 0

            for item in medications_data:
                medication_name = item['medication_name']
                quantity = item['quantity']

                try:
                    medication = Medications.objects.get(name=medication_name)
                except Medications.DoesNotExist:
                    return Response(
                        data={"error": f"""Medication '{medication_name}' 
                        is not available in the database."""},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                if medication.stock_quantity < quantity:
                    return Response(
                        data={"error": f"""Not enough stock for 
                        '{medication_name}'. Available: {medication.stock_quantity}"""},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                BasketItem.objects.create(
                    basket=basket,
                    medication=medication,
                    quantity=quantity
                )

                item_total_price = medication.price * quantity
                total_price += item_total_price

                response_data.append({
                    "medication_name": medication.name,
                    "quantity": quantity,
                    "price": medication.price,
                    "total_price": item_total_price
                })

                medication.stock_quantity -= quantity
                medication.save()

            return Response(
                {
                    "full_name": user.full_name,
                    "created_at": basket.created_at,
                    "items": response_data,
                    "total_price": total_price
                },
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ViewBasketView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BasketDetailSerializer

    @swagger_auto_schema(
        operation_summary="Get User's Basket",
        operation_description= "Retrieve all baskets for the authenticated user.",
        responses={
            200: openapi.Response(
                description="List of baskets for the user",
                schema=BasketDetailSerializer(many=True)
            ),
            404: openapi.Response(
                description="No baskets found for the user")
        }
    )
    def get(self, request, *args, **kwargs):
        baskets = Basket.objects.filter(
            user=request.user).order_by('-created_at')

        if not baskets.exists():
            return Response(
                data={"message": "You do not have any baskets."},
                status=404)

        serializer = BasketDetailSerializer(baskets, many=True)
        return Response(serializer.data, status=200)


class BasketItemModelViewSet(ModelViewSet):
    permission_classes = [IsAdminReadOnly]
    queryset = BasketItem.objects.all()
    serializer_class = BasketItemAdminSerializer
