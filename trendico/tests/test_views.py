from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from trendico.forms import SignUpForm
from trendico.models import ProductCategory, Product, Wishlist, Cart, CartItem


class HomeViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = ProductCategory.objects.create(name='Test Category')
        self.product1 = Product.objects.create(
            name='Product 1', price=10.00, initial_quantity=10, category=self.category)
        self.product2 = Product.objects.create(
            name='Product 2', price=15.00, initial_quantity=5, category=self.category)

    def test_home_view(self):
        url = reverse('home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
        self.assertEqual(
            len(response.context['categories']), ProductCategory.objects.count())
        self.assertEqual(
            len(response.context['Products']), Product.objects.count())
        self.assertIsNone(response.context['selected_category'])


class RemoveFromCartViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')
        self.cart = Cart.objects.create(user=self.user)
        self.cart_item = CartItem.objects.create(
            cart=self.cart, product_id=1, quantity=2)

    def test_remove_cart_item(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(
            '/remove_from_cart/{}/'.format(self.cart_item.id))
        self.assertEqual(response.status_code, 200)


class RemoveFromWishlistViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')
        self.category = ProductCategory.objects.create(
            name='Test Category')  # Create a category instance
        self.product = Product.objects.create(
            name='Test Product', price=10.00, initial_quantity=10, category=self.category)
        self.wishlist = Wishlist.objects.create(user=self.user)
        self.wishlist.items.add(self.product)

    def test_remove_wishlist_item(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(
            reverse('remove_from_wishlist', args=[self.product.id]))
        self.assertEqual(response.status_code, 200)


class TestLaptopCategoryView(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = 'Laptop'

    def test_laptop_category_view(self):
        url = reverse('product-category', args=[self.category])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class TestTabCategoryView(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = 'Tab'

    def test_tab_category_view(self):
        url = reverse('product-category', args=[self.category])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class TestHeadphonesCategoryView(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = 'Headphones'

    def test_headphones_category_view(self):
        url = reverse('product-category', args=[self.category])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class ProductViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = ProductCategory.objects.create(
            name='Test Category')  # Create a category instance
        self.product = Product.objects.create(
            name='Test Product', price=10.00, initial_quantity=10, category=self.category)  # Provide valid category value
        self.url = reverse('product', args=[self.product.name])

    def test_product_view_exists(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_product_view_uses_correct_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'product.html')


class LoginViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')
        self.url = reverse('login')

    def test_login_view_exists(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_login_view_uses_correct_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'login.html')

    def test_login_view_successful_login(self):
        response = self.client.post(
            self.url, {'username': 'testuser', 'password': 'testpassword'})
        self.assertRedirects(response, reverse('home'))


class LogoutViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.url = reverse('logout')

    def test_logout_view_successful_logout(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse('home'))


class RegisterViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('register')
        self.valid_data = {
            'username': 'testuser',
            'password1': 'testpassword',
            'password2': 'testpassword',
            'full_name': 'Test User',
            'email': 'testuser@example.com',
        }

    def test_register_view_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
        self.assertIsInstance(response.context['form'], SignUpForm)

    def test_register_view_post_success(self):
        form = SignUpForm(data=self.valid_data)
        self.assertTrue(form.is_valid(), form.errors)

        response = self.client.post(self.url, self.valid_data, follow=True)
        self.assertEqual(response.status_code, 200)
