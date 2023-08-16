from django.test import TestCase
from django.contrib.auth.models import User
from trendico.models import ProductCategory, Product, ProductImage, EventType, Stock, UserReview, TopSellingProduct, Cart,CartItem, Wishlist, Order

class ProductCategoryTest(TestCase):
    def test_string_representation(self):
        category = ProductCategory(name='Electronics', description='Electronics category')
        self.assertEqual(str(category), 'Electronics')

class ProductTest(TestCase):
    def setUp(self):
        self.category = ProductCategory.objects.create(name='Electronics', description='Electronics category')
        self.product = Product.objects.create(name='Laptop', price=1000.00, category=self.category, initial_quantity=10)

    def test_string_representation(self):
        self.assertEqual(str(self.product), 'Laptop')

    def test_discount_percentage(self):

        self.product.discount_price = 800.00
        self.assertEqual(self.product.discount_percentage, 20)

        self.product.price = 0
        self.assertEqual(self.product.discount_percentage, 0)

class ProductImageTest(TestCase):
    def setUp(self):
        self.category = ProductCategory.objects.create(name='Electronics', description='Electronics category')
        self.product = Product.objects.create(name='Laptop', price=1000.00, category=self.category, initial_quantity=10)
        self.image = ProductImage.objects.create(product=self.product, image='laptop.jpg')

    def test_string_representation(self):
        self.assertEqual(str(self.image), 'Image for Laptop')


class EventTypeTest(TestCase):
    def test_string_representation(self):
        event_type = EventType(name='Purchase')
        self.assertEqual(str(event_type), 'Purchase')


class TopSellingProductTest(TestCase):
    def setUp(self):
        self.category = ProductCategory.objects.create(name='Electronics', description='Electronics category')
        self.product = Product.objects.create(name='Laptop', price=1000.00, category=self.category, initial_quantity=10)
        self.top_selling_product = TopSellingProduct.objects.create(product=self.product, total_revenue=5000.00,
                                                                    sales_count=5)

    def test_string_representation(self):
        self.assertEqual(str(self.top_selling_product), f'{self.product.name}')
class CartTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.cart = Cart.objects.create(user=self.user)

    def test_string_representation(self):
        expected_representation = f'Cart object ({self.cart.id})'
        self.assertEqual(str(self.cart), expected_representation)


class CartItemTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.category = ProductCategory.objects.create(name='Electronics', description='Electronics category')
        self.product = Product.objects.create(name='Laptop', price=1000.00, category=self.category, initial_quantity=10)
        self.cart = Cart.objects.create(user=self.user)
        self.cart_item = CartItem.objects.create(cart=self.cart, product=self.product, quantity=2)

    def test_cart_item_attributes(self):
        self.assertEqual(self.cart_item.cart, self.cart)
        self.assertEqual(self.cart_item.product, self.product)
        self.assertEqual(self.cart_item.quantity, 2)

class WishlistTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.category = ProductCategory.objects.create(name='Electronics', description='Electronics category')
        self.product = Product.objects.create(name='Laptop', price=1000.00, category=self.category, initial_quantity=10)
        self.wishlist = Wishlist.objects.create(user=self.user)
        self.wishlist.items.add(self.product)

    def test_string_representation(self):
        self.assertEqual(str(self.wishlist), f'Wishlist of {self.user.username}')

class OrderTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
