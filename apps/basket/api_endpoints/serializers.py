from rest_framework import serializers

from apps.account_.models import Users
from apps.basket.models import BasketItem, Basket
from apps.medication.models import Medications


class BasketItemAdminSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = BasketItem
        fields = ['id', 'basket', 'medication', 'quantity', 'user']

    def get_user(self, obj):
        return obj.basket.user.email if obj.basket else None


class MedicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medications
        fields = ('name', 'price', 'stock_quantity')


class BasketItemSerializer(serializers.Serializer):
    medication_name = serializers.CharField()
    quantity = serializers.IntegerField(min_value=1)


class BasketResponseSerializer(serializers.Serializer):
    medication_name = serializers.CharField()
    quantity = serializers.IntegerField()
    price = serializers.FloatField()
    total_price = serializers.FloatField()


class BasketCreateSerializer(serializers.Serializer):
    medications = BasketItemSerializer(many=True)


class BasketItemDetailSerializer(serializers.ModelSerializer):
    medication_name = serializers.CharField(source="medication.name")
    price = serializers.FloatField(source="medication.price")

    class Meta:
        model = BasketItem
        fields = ("medication_name", "quantity", "price")


class BasketDetailSerializer(serializers.ModelSerializer):
    items = BasketItemDetailSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Basket
        fields = ("id", "created_at", "updated_at", "items", "total_price")

    def get_total_price(self, obj):
        return (
            sum(item.quantity * item.medication.price
                for item in obj.items.all()))
