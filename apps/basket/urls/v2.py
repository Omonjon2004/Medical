from rest_framework.routers import DefaultRouter

from apps.basket.api_endpoints import BasketItemModelViewSet

router = DefaultRouter()
router.register('baskets', BasketItemModelViewSet)

urlpatterns = router.urls
