from warehouse.api.views import SupplierViewSet, CategoryViewSet, ProductViewSet, ProductQuantityViewSet, OrderViewSet, OrderItemViewSet, WarehouseViewSet, WarehouseItemViewSet

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'suppliers', SupplierViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'products', ProductViewSet)
router.register(r'product-quantities', ProductQuantityViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'order-items', OrderItemViewSet)
router.register(r'warehouses', WarehouseViewSet)
router.register(r'warehouse-items', WarehouseItemViewSet)

urlpatterns = router.urls