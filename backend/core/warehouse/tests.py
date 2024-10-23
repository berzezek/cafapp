from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from warehouse.models import Supplier, Category, Product, ProductQuantity, Order, OrderItem, Warehouse, WarehouseItem

class AuthTests(APITestCase):
    def setUp(self):
        self.auth_url = '/api/token/'
        self.auth_data = {'username': 'berzezek', 'password': 'foo'}
        self.create_user()
        self.auth_user()

    def create_user(self):
        User.objects.create_user(username=self.auth_data['username'], password=self.auth_data['password'])

    def auth_user(self):
        auth_response = self.client.post(self.auth_url, self.auth_data, format='json')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + auth_response.data['access'])

class SupplierTests(AuthTests):
    
    def setUp(self):
        super().setUp()
        self.item_data = {'name': 'Test Item', 'email': 'test@supplier.com', 'phone': '1234567890', 'address': 'Test address'}
        self.update_data = {'name': 'Updated Item'}
        self.url = '/api/v1/suppliers/'


    def test_create_item(self):
        response = self.client.post(self.url, self.item_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Supplier.objects.count(), 1)
        self.assertEqual(Supplier.objects.get().name, 'Test Item')
        self.assertEqual(Supplier.objects.get().email, 'test@supplier.com')
        self.assertEqual(Supplier.objects.get().phone, '1234567890')
        self.assertEqual(Supplier.objects.get().address, 'Test address')

    def test_get_items(self):
        Supplier.objects.create(name='Test Item')
        
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_get_item(self):
        Supplier.objects.create(name='Test Item')
        
        supplier = Supplier.objects.get(name='Test Item')
        response = self.client.get(f'{self.url}{supplier.id}/', format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Item')

    def test_update_items(self):
        Supplier.objects.create(name=self.item_data['name'])

        supplier = Supplier.objects.get(name='Test Item')
        response = self.client.put(f'{self.url}{supplier.id}/', self.update_data, format='json')
        supplier.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(supplier.name, 'Updated Item')

    def test_delete_items(self):
        Supplier.objects.create(name='Test Item')

        supplier = Supplier.objects.get(name='Test Item')
        response = self.client.delete(f'{self.url}{supplier.id}/', format='json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Supplier.objects.count(), 0)

    
class CategoryTests(AuthTests):
    def setUp(self):
        super().setUp()
        self.item_data = {'name': 'New test Item', 'description': 'Test description'}
        self.update_data = {'name': 'Updated Item'}
        self.url = '/api/v1/categories/'
        self.create_category()

    def test_create_item(self):
        response = self.client.post(self.url, self.item_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 2)
        self.assertEqual(Category.objects.last().name, 'New test Item')
        self.assertEqual(Category.objects.last().description, 'Test description')

    def create_category(self):
        Category.objects.create(name='Test Item')

    def test_get_items(self):
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_get_item(self):
        category = Category.objects.get(name='Test Item')
        response = self.client.get(f'{self.url}{category.id}/', format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Item')
    
    def test_update_items(self):
        category = Category.objects.get(name='Test Item')
        response = self.client.put(f'{self.url}{category.id}/', self.update_data, format='json')
        category.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(category.name, 'Updated Item')

    def test_delete_items(self):
        category = Category.objects.get(name='Test Item')
        response = self.client.delete(f'{self.url}{category.id}/', format='json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Category.objects.count(), 0)


class ProductTest(AuthTests):

    def setUp(self):
        super().setUp()
        self.item_data = {'name': 'New test Item', 'description': 'Test description', 'price': 10.0}
        self.update_data = {'name': 'Updated Item', 'price': 20.0}
        self.url = '/api/v1/products/'
        self.category = None
        self.supplier = None
        self.add_category_supplier()
        self.create_product()

    def set_category(self):
        self.category = Category.objects.create(name='Test Category')

    def set_supplier(self):
        self.supplier = Supplier.objects.create(name='Test Supplier')

    def add_category_supplier(self):
        self.set_category()
        self.set_supplier()
        self.item_data['category'] = self.category.id
        self.item_data['supplier'] = self.supplier.id

    def create_product(self):
        Product.objects.create(
            name='Test Item',
            description='Test description',
            price=20.0,
            category=self.category,
            supplier=self.supplier
        )


    def test_create_item(self):
        response = self.client.post(self.url, self.item_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 2)
        self.assertEqual(Product.objects.last().name, 'New test Item')
        self.assertEqual(Product.objects.last().description, 'Test description')
        self.assertEqual(Product.objects.last().price, 10.0)

    def test_get_items(self):
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_get_item(self):
        product = Product.objects.get(name='Test Item')
        response = self.client.get(f'{self.url}{product.id}/', format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Item')

    def test_update_items(self):
        product = Product.objects.get(name='Test Item')
        response = self.client.put(f'{self.url}{product.id}/', self.update_data, format='json')
        product.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(product.name, 'Updated Item')

    def test_delete_items(self):
        product = Product.objects.get(name='Test Item')
        response = self.client.delete(f'{self.url}{product.id}/', format='json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.count(), 0)


class ProductQuantityTest(AuthTests):

    def setUp(self):
        super().setUp()
        self.product = None
        self.category = None
        self.supplier = None
        self.product_data = {'name': 'New test Item', 'description': 'Test description', 'price': 10.0}
        self.item_data = {'product': None, 'quantity': 10}
        self.update_data = {'quantity': 20}
        self.url = '/api/v1/product-quantities/'
        self.create_product()
        self.create_product_quantity()

    def set_category(self):
        self.category = Category.objects.create(name='Test Category')

    def set_supplier(self):
        self.supplier = Supplier.objects.create(name='Test Supplier')

    def add_category_supplier(self):
        self.set_category()
        self.set_supplier()
        self.item_data['category'] = self.category.id
        self.item_data['supplier'] = self.supplier.id

    def create_product(self):
        self.add_category_supplier()
        self.product = Product.objects.create(
            name='Test Item',
            description='Test description',
            price=20.0,
            category=self.category,
            supplier=self.supplier
        )
        self.item_data['product'] = self.product.id

    def create_product_quantity(self):
        ProductQuantity.objects.create(
            product=self.product,
            quantity=self.item_data['quantity']
        )


    def test_create_item(self):
        response = self.client.post(self.url, self.item_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ProductQuantity.objects.count(), 2)
        self.assertEqual(ProductQuantity.objects.last().product.name, 'Test Item')
        self.assertEqual(ProductQuantity.objects.last().quantity, 10)

    def test_get_items(self):
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_get_item(self):
        product_quantity = ProductQuantity.objects.get(product=self.product)
        response = self.client.get(f'{self.url}{product_quantity.id}/', format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['product'], self.product.id)
        self.assertEqual(response.data['quantity'], 10)

    def test_update_items(self):
        product_quantity = ProductQuantity.objects.get(product=self.product)
        self.update_data['product'] = self.product.id
        response = self.client.put(f'{self.url}{product_quantity.id}/', self.update_data, format='json')
        product_quantity.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(product_quantity.quantity, 20)

    def test_delete_items(self):
        product_quantity = ProductQuantity.objects.get(product=self.product)
        response = self.client.delete(f'{self.url}{product_quantity.id}/', format='json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(ProductQuantity.objects.count(), 0)


class OrderTest(AuthTests):
    
        def setUp(self):
            super().setUp()
            self.order = None
            self.product_quantity = None
            self.item_data = {'stage': 'Draft', 'description': 'Test description'}
            self.update_data = {'stage': 'Confirmed'}
            self.url = '/api/v1/orders/'
            self.create_order()
    
        def create_order(self):
            Order.objects.create(
                stage='Draft',
                description='Test description'
            )
    
        def test_create_item(self):
            response = self.client.post(self.url, self.item_data, format='json')
    
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(Order.objects.count(), 2)
            self.assertEqual(Order.objects.last().stage, 'Draft')
            self.assertEqual(Order.objects.last().description, 'Test description')
    
        def test_get_items(self):
            response = self.client.get(self.url, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(len(response.data['results']), 1)
    
        def test_get_item(self):
            order = Order.objects.get(stage='Draft')
            response = self.client.get(f'{self.url}{order.id}/', format='json')
    
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data['stage'], 'Draft')
    
        def test_update_items(self):
            order = Order.objects.get(stage='Draft')
            response = self.client.put(f'{self.url}{order.id}/', self.update_data, format='json')
            order.refresh_from_db()
    
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(order.stage, 'Confirmed')
    
        def test_delete_items(self):
            order = Order.objects.get(stage='Draft')
            response = self.client.delete(f'{self.url}{order.id}/', format='json')
    
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
            self.assertEqual(Order.objects.count(), 0)

class OrderItemTest(AuthTests):
    
    # order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    # product_quantity = models.ForeignKey(ProductQuantity, on_delete=models.CASCADE)

    def setUp(self):
        super().setUp()
        self.item_data = {'order': None, 'product_quantity': None}
        self.url = '/api/v1/order-items/'
        self.create_order_item()

    def set_category(self):
        return Category.objects.create(name='Test Category')

    def set_supplier(self):
        return Supplier.objects.create(name='Test Supplier')

    def set_product(self):
        return Product.objects.create(
            name='Test Item',
            description='Test description',
            price=20.0,
            category=self.set_category(),
            supplier=self.set_supplier()
        )

    def set_product_quantity(self):
        self.product_quantity = ProductQuantity.objects.create(
            product=self.set_product(),
            quantity=20.0
        )

    def set_order(self):
        self.order = Order.objects.create(
            stage='Draft',
            description='Test description'
        )

    def create_order_item(self):
        self.set_order()
        self.set_product_quantity()
        OrderItem.objects.create(
            order=self.order,
            product_quantity=self.product_quantity
        )

    def test_create_item(self):
        self.item_data['order'] = self.order.id
        self.item_data['product_quantity'] = self.product_quantity.id
        response = self.client.post(self.url, self.item_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(OrderItem.objects.count(), 2)
        self.assertEqual(OrderItem.objects.last().order.stage, 'Draft')
        self.assertEqual(OrderItem.objects.last().product_quantity.product.name, 'Test Item')

    def test_get_items(self):
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    
    def test_get_item(self):
        order_item = OrderItem.objects.get(order=self.order)
        response = self.client.get(f'{self.url}{order_item.id}/', format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['order'], self.order.id)
        self.assertEqual(response.data['product_quantity'], self.product_quantity.id)

    def test_update_items(self):
        order_item = OrderItem.objects.get(order=self.order)
        new_order = Order.objects.create(
            stage='Confirmed',
            description='Test description'
        )
        update_data = {'order': new_order.id}
        response = self.client.patch(f'{self.url}{order_item.id}/', update_data, format='json')
        order_item.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_items(self):
        order_item = OrderItem.objects.get(order=self.order)
        response = self.client.delete(f'{self.url}{order_item.id}/', format='json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(OrderItem.objects.count(), 0)

class WarehouseTest(AuthTests):
    def setUp(self):
        super().setUp()
        self.item_data = {'name': 'Test Item'}
        self.update_data = {'name': 'Updated Item'}
        self.url = '/api/v1/warehouses/'
        self.create_warehouse()

    def create_warehouse(self):
        Warehouse.objects.create(name='Test Item')

    def test_create_item(self):
        response = self.client.post(self.url, self.item_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Warehouse.objects.count(), 2)
        self.assertEqual(Warehouse.objects.last().name, 'Test Item')

    def test_get_items(self):
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_get_item(self):
        warehouse = Warehouse.objects.get(name='Test Item')
        response = self.client.get(f'{self.url}{warehouse.id}/', format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Item')

    def test_update_items(self):
        warehouse = Warehouse.objects.get(name='Test Item')
        response = self.client.put(f'{self.url}{warehouse.id}/', self.update_data, format='json')
        warehouse.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(warehouse.name, 'Updated Item')

    def test_delete_items(self):
        warehouse = Warehouse.objects.get(name='Test Item')
        response = self.client.delete(f'{self.url}{warehouse.id}/', format='json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Warehouse.objects.count(), 0)


class WarehouseItemTest(AuthTests):
    def setUp(self):
        super().setUp()
        self.warehouse = None
        self.product_quantity = None
        self.item_data = {'warehouse': None, 'product_quantity': None}
        self.url = '/api/v1/warehouse-items/'
        self.create_warehouse_item()

    def set_category(self):
        return Category.objects.create(name='Test Category')

    def set_supplier(self):
        return Supplier.objects.create(name='Test Supplier')

    def set_product(self):
        return Product.objects.create(
            name='Test Item',
            description='Test description',
            price=20.0,
            category=self.set_category(),
            supplier=self.set_supplier()
        )

    def set_product_quantity(self):
        return ProductQuantity.objects.create(
            product=self.set_product(),
            quantity=20.0
        )

    def set_warehouse(self):
        return Warehouse.objects.create(
            name='Test Item'
        )

    def create_warehouse_item(self):
        self.warehouse = self.set_warehouse()
        self.product_quantity = self.set_product_quantity()
        WarehouseItem.objects.create(
            warehouse=self.warehouse,
            product_quantity=self.product_quantity
        )

    def test_create_item(self):
        self.item_data['warehouse'] = self.warehouse.id
        self.item_data['product_quantity'] = self.product_quantity.id
        response = self.client.post(self.url, self.item_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(WarehouseItem.objects.count(), 2)
        self.assertEqual(WarehouseItem.objects.last().warehouse.name, 'Test Item')
        self.assertEqual(WarehouseItem.objects.last().product_quantity.product.name, 'Test Item')

    def test_get_items(self):
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    
    def test_get_item(self):
        warehouse_item = WarehouseItem.objects.get(warehouse=self.warehouse)
        response = self.client.get(f'{self.url}{warehouse_item.id}/', format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['warehouse'], self.warehouse.id)
        self.assertEqual(response.data['product_quantity'], self.product_quantity.id)

    def test_update_items(self):
        warehouse_item = WarehouseItem.objects.get(warehouse=self.warehouse)
        new_item = ProductQuantity.objects.create(
            product=self.set_product(),
            quantity=10.0
        )
        update_data = {'product_quantity': new_item.id}
        response = self.client.patch(f'{self.url}{warehouse_item.id}/', update_data, format='json')
        warehouse_item.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(warehouse_item.product_quantity.quantity, 10)

    def test_delete_items(self):
        warehouse_item = WarehouseItem.objects.get(warehouse=self.warehouse)
        response = self.client.delete(f'{self.url}{warehouse_item.id}/', format='json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(WarehouseItem.objects.count(), 0)