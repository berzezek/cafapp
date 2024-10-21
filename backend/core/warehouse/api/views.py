from warehouse.models import Supplier, Category, Product, ProductQuantity, Order, OrderItem, Warehouse, WarehouseItem
from warehouse.api.serializers import SupplierSerializer, CategorySerializer, ProductSerializer, ProductQuantitySerializer, OrderSerializer, OrderItemSerializer, WarehouseSerializer, WarehouseItemSerializer

from rest_framework import viewsets


class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductQuantityViewSet(viewsets.ModelViewSet):
    queryset = ProductQuantity.objects.all()
    serializer_class = ProductQuantitySerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer


class WarehouseViewSet(viewsets.ModelViewSet):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer


class WarehouseItemViewSet(viewsets.ModelViewSet):
    queryset = WarehouseItem.objects.all()
    serializer_class = WarehouseItemSerializer