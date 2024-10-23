from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


from warehouse.models import Supplier, Category, Product, ProductQuantity, Order, OrderItem, Warehouse, WarehouseItem
from warehouse.api.serializers import (
    SupplierSerializer, 
    CategorySerializer, 
    ProductSerializer, 
    ProductQuantitySerializer, 
    OrderSerializer, 
    OrderItemSerializer, 
    WarehouseSerializer, 
    WarehouseItemSerializer
)



class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [IsAuthenticated]


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]



class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]


class ProductQuantityViewSet(viewsets.ModelViewSet):
    queryset = ProductQuantity.objects.all()
    serializer_class = ProductQuantitySerializer
    permission_classes = [IsAuthenticated]


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]


class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]


class WarehouseViewSet(viewsets.ModelViewSet):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer
    permission_classes = [IsAuthenticated]


class WarehouseItemViewSet(viewsets.ModelViewSet):
    queryset = WarehouseItem.objects.all()
    serializer_class = WarehouseItemSerializer
    permission_classes = [IsAuthenticated]


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def warehouse_items(request, warehouse_pk):
    paginator = PageNumberPagination()
    paginator.page_size = 10
    warehouse_items = WarehouseItem.objects.filter(warehouse=warehouse_pk)
    result_page = paginator.paginate_queryset(warehouse_items, request)
    serializer = WarehouseItemSerializer(warehouse_items, many=True)
    return paginator.get_paginated_response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def order_items(request, order_pk):
    paginator = PageNumberPagination()
    paginator.page_size = 10
    order_items = OrderItem.objects.filter(order=order_pk)
    result_page = paginator.paginate_queryset(order_items, request)
    serializer = OrderItemSerializer(order_items, many=True)
    return paginator.get_paginated_response(serializer.data)