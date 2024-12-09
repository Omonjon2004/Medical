from django.urls import path

from apps.basket.api_endpoints import AddToBasketView, ViewBasketView

urlpatterns = [
    path('add-to-basket/', AddToBasketView.as_view(), name='add-to-basket'),
    path('view-basket/', ViewBasketView.as_view(), name='view-basket'),
]
