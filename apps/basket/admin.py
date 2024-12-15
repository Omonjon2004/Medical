from django.contrib import admin

from apps.basket.models import Basket, BasketItem


@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    search_fields = (
        "id",
        "user__full_name",
        "created_at",
        "updated_at"
    )
    list_display = (
        "id",
        "user",
        "created_at",
        "updated_at"
    )


@admin.register(BasketItem)
class BasketItemAdmin(admin.ModelAdmin):
    search_fields = (
        "id",
        "medication__name",
        "quantity",
        "added_at"
    )
    list_display = (
        "id",
        "medication",
        "quantity",
        "added_at"
    )
