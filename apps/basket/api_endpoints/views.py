from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.basket.models import Basket, BasketItem
from apps.medication.models import Medications


class AddToBasketView(APIView):
    def post(self, request):
        user = request.user  # Tizimga kirgan foydalanuvchi
        medication_id = request.data.get('medication_id')
        quantity = request.data.get('quantity', 1)

        # Foydalanuvchi mavjudligini tekshirish
        if not user.is_authenticated:
            return Response(
                data={"error": "User must be logged in"},
                status=status.HTTP_400_BAD_REQUEST)

        # Dori mavjudligini tekshirish
        try:
            medication = Medications.objects.get(id=medication_id)
        except Medications.DoesNotExist:
            return Response(
                data={"error": "Medication not found"},
                status=status.HTTP_404_NOT_FOUND)

        # Dorining stock_quantity miqdorini tekshirish
        if medication.stock_quantity < quantity:
            return Response(
                data={"error": "Not enough stock available"},
                status=status.HTTP_400_BAD_REQUEST)

        # Foydalanuvchining savatini olish yoki yaratish
        basket, created = Basket.objects.get_or_create(user=user)

        # Savatga mahsulot qo'shish yoki mavjud bo'lsa, miqdorini yangilash
        basket_item, created = BasketItem.objects.get_or_create(
            basket=basket,
            medication=medication)

        if not created:
            # Agar mahsulot mavjud bo'lsa, miqdorni yangilash
            basket_item.quantity += quantity
            basket_item.save()

        # Dorining stock_quantity ni kamaytirish
        medication.stock_quantity -= quantity
        medication.save()

        # Jami narxni hisoblash
        total_price = basket_item.total_price

        return Response({
            "message": "Medication added to basket",
            "medication_name": medication.name,
            "quantity": basket_item.quantity,
            "total_price": total_price
        }, status=status.HTTP_200_OK)


class ViewBasketView(APIView):
    def get(self, request):
        user = request.user  # Tizimga kirgan foydalanuvchi
        if not user.is_authenticated:
            return Response(
                data={"error": "User must be logged in"},
                status=status.HTTP_400_BAD_REQUEST)

        # Foydalanuvchining savatini olish
        try:
            basket = Basket.objects.get(user=user)
        except Basket.DoesNotExist:
            return Response(
                data={"message": "Basket is empty"},
                status=status.HTTP_200_OK)

        basket_items = basket.items.all()
        total_price = sum(item.total_price for item in basket_items)

        items_data = [{
            'medication_name': item.medication.name,
            'quantity': item.quantity,
            'description': item.medication.description,
            'price_per_unit': item.medication.price,
            'total_price': item.total_price
        } for item in basket_items]

        return Response({
            'items': items_data,
            'total_price': total_price
        }, status=status.HTTP_200_OK)
