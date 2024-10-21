from django.db import models


class Supplier(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254, null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    address = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name


class ProductQuantity(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"


class Order(models.Model):
    STAGE_CHOICES = (
        ('Draft', 'Draft'),
        ('Confirmed', 'Confirmed'),
        ('Paid', 'Paid'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
        ('Trash', 'Trash'),
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    stage = models.CharField(max_length=50, choices=STAGE_CHOICES, default='Draft')
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'Order {self.id}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product_quantity = models.ForeignKey(ProductQuantity, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.order} - {self.product_quantity.product.name}"


class Warehouse(models.Model):
    name = models.CharField(max_length=50)
    address = models.TextField(null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)

    def __str__(self):
        return self.name


class WarehouseItem(models.Model):
    product_quantity = models.ForeignKey(ProductQuantity, on_delete=models.CASCADE)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.product_quantity.product.name} in {self.warehouse.name}"
