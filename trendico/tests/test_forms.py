from django.test import TestCase
from trendico.forms import SignUpForm, OrderForm

class SignUpFormTest(TestCase):
    def test_signup_form_valid_data(self):
        form = SignUpForm({
            'username': 'testuser',
            'full_name': 'Test User',
            'email': 'test@example.com',
            'password1': 'testpassword',
            'password2': 'testpassword',
        })
        self.assertTrue(form.is_valid())

    def test_signup_form_missing_data(self):
        form = SignUpForm({
            'username': '',
            'full_name': '',
            'email': '',
            'password1': '',
            'password2': '',
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 5)
class OrderFormTest(TestCase):
    def test_order_form_valid_data(self):
        form = OrderForm({
            'billing_first_name': 'John',
            'billing_last_name': 'Doe',
            'billing_email': 'john@example.com',
            'billing_address': '123 Main St',
            'billing_city': 'City',
            'billing_country': 'Country',
            'billing_zip_code': '12345',
            'billing_tel': '555-1234',
        })
        self.assertTrue(form.is_valid())

    def test_order_form_missing_data(self):
        form = OrderForm({})
        self.assertFalse(form.is_valid())
