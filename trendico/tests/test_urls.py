from django.test import SimpleTestCase
from django.urls import reverse,resolve
from trendico.views import HomeView,LoginView,LogoutView,RegisterView,CartView,CheckoutView,RemoveFromCartView,RemoveFromWishlistView,ProductView

class TestUrls(SimpleTestCase):
    def test_home_url_is_resolved(self):
        url=reverse('home')
        self.assertEquals(resolve(url).func.view_class,HomeView)

    def test_login_url_is_resolved(self):
        url = reverse('login')
        self.assertEquals(resolve(url).func.view_class, LoginView)

    def test_logout_url_is_resolved(self):
        url = reverse('logout')
        self.assertEquals(resolve(url).func.view_class, LogoutView)

    def test_register_url_is_resolved(self):
        url = reverse('register')
        self.assertEquals(resolve(url).func.view_class, RegisterView)

    def test_cart_url_is_resolved(self):
        url = reverse('cart')
        self.assertEquals(resolve(url).func.view_class, CartView)

    def test_checkout_url_is_resolved(self):
        url = reverse('checkout')
        self.assertEquals(resolve(url).func.view_class, CheckoutView)

    def test_remove_from_cart_url_is_resolved(self):
        url = reverse('remove_from_cart', args=[1])
        self.assertEquals(resolve(url).func.view_class, RemoveFromCartView)

    def test_remove_from_wishlist_url_is_resolved(self):
        url = reverse('remove_from_wishlist', args=[1])
        self.assertEquals(resolve(url).func.view_class, RemoveFromWishlistView)

    def test_product_url_is_resolved(self):
        product_names = ['product1', 'product2', 'product3']
        for name in product_names:
            url = reverse('product', args=[name])
            self.assertEquals(resolve(url).func.view_class, ProductView)