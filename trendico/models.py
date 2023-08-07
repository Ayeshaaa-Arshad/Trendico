from datetime import datetime, timedelta
from django.db import models

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    class Meta:
        abstract = True

class ProductCategory(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.name

class Product(BaseModel):
    name = models.CharField(max_length=50)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    description = models.TextField()
    initial_quantity = models.PositiveIntegerField()

    def __str__(self):
        return self.name

    @property
    def is_new(self):
        created_at_naive = self.created_at.replace(tzinfo=None)
        time_difference = datetime.now() - created_at_naive
        return time_difference < timedelta(days=15)

    @property
    def discount_percentage(self):
        if self.price is None or self.discount_price is None:
            return 0
        elif self.price <= 0 or self.discount_price <= 0:
            return 0
        else:
            discount_amount = self.price - self.discount_price
            discount_percentage = round((discount_amount / self.price) * 100)
            return discount_percentage

    @classmethod
    def get_specific_products(cls, category):
        if category.lower() == 'all':
            return cls.objects.all()

        selected_category = ProductCategory.objects.filter(name__iexact=category).first()
        if selected_category:
            return cls.objects.filter(category=selected_category)

        return cls.objects.none()

class ProductImage(BaseModel):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images')
    def __str__(self):
        return f"Image for {self.product.name}"

class Stock(models.Model):
    product = models.ForeignKey(Product,related_name='stocks', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    event_type = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.product.name} - {self.event_type} - {self.timestamp}"
