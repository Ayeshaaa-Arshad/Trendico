from django.db import models
from datetime import datetime, timedelta
# Create your models here.
CATEGORY_CHOICES = (
    ('L', 'Laptop'),
    ('T', 'Tab'),
    ('C', 'Camera'),
    ('H', 'Headphone')
)
class Product(models.Model):
    product_name=models.CharField(max_length=50)
    img_URL = models.ImageField(upload_to='images')
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=1)
    description = models.TextField()
    total_quantity=models.PositiveIntegerField()
    created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return(f"{self.product_name} {self.price}")

    @classmethod
    def is_new(cls,products):
        for product in products:
            created_at_naive = product.created_at.replace(tzinfo=None)
            time_difference = datetime.now() - created_at_naive
            product.isNew = time_difference < timedelta(days=15)

    @classmethod
    def calculate_discount_percentage(cls,products):
        for product in products:
            if product.price is None or product.discount_price is None:
                product.discount_percentage = 0
            elif product.price <= 0 or product.discount_price <= 0:
                product.discount_percentage = 0
            else:
                discount_amount = product.price - product.discount_price
                product.discount_percentage = (discount_amount / product.price) * 100

class TopSellingProduct(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    total_sales_quantity = models.PositiveIntegerField()
    total_revenue = models.DecimalField(max_digits=10, decimal_places=2)
    profit_margin = models.DecimalField(max_digits=5, decimal_places=2)
    customer_ratings = models.DecimalField(max_digits=3, decimal_places=2)
    promotional_success = models.BooleanField()
    market_trends = models.BooleanField()
    last_updated = models.DateTimeField(auto_now=True)
