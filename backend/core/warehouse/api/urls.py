from django.urls import path
from rest_framework.routers import DefaultRouter

app_name = 'warehouse'

from warehouse.api.views import (
    SupplierViewSet, 
    CategoryViewSet, 
    ProductViewSet, 
    ProductQuantityViewSet, 
    OrderViewSet, 
    OrderItemViewSet, 
    WarehouseViewSet, 
    WarehouseItemViewSet,
    warehouse_items,
    order_items
)


router = DefaultRouter()
router.register(r'suppliers', SupplierViewSet, basename='supplier')
router.register(r'categories', CategoryViewSet)
router.register(r'products', ProductViewSet)
router.register(r'product-quantities', ProductQuantityViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'order-items', OrderItemViewSet)
router.register(r'warehouses', WarehouseViewSet)
router.register(r'warehouse-items', WarehouseItemViewSet)

urlpatterns = [
    path('items/<int:warehouse_pk>/', warehouse_items, name='warehouse-items'),
    path('order/<int:order_pk>/', order_items, name='order-items'),
]

urlpatterns += router.urls