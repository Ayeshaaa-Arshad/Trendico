from datetime import datetime, timedelta
from django.db.models.signals import post_save
from django.dispatch import receiver
from decimal import Decimal
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import User


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

    @property
    def average_rating(self):
        if self.user_reviews.exists():
            return self.user_reviews.aggregate(models.Avg('star_rating'))['star_rating__avg']
        return 0

    @property
    def is_top_seller(self):
        try:
            top_selling_product = TopSellingProduct.objects.get(product=self)
            return top_selling_product.sales_count >= 5 and self.average_rating >= 3
        except TopSellingProduct.DoesNotExist:
            return False

    @classmethod
    def get_specific_products(cls, category):
        if category.lower() == 'all':
            return cls.objects.all()

        selected_category = ProductCategory.objects.filter(
            name__iexact=category).first()
        if selected_category:
            return cls.objects.filter(category=selected_category)

        return cls.objects.none()


@receiver(post_save, sender=Product)
def create_top_selling_product(sender, instance, created, **kwargs):
    if created:
        top_selling_product, created = TopSellingProduct.objects.get_or_create(
            product=instance)


class ProductImage(BaseModel):
    product = models.ForeignKey(
        Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images')

    def __str__(self):
        return f"Image for {self.product.name}"


class EventType(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name


class Stock(models.Model):
    product = models.ForeignKey(
        Product, related_name='stocks', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    event_type = models.ForeignKey(
        EventType, related_name='stock_events', on_delete=models.CASCADE)


class UserReview(BaseModel):
    product = models.ForeignKey(
        Product, related_name='user_reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    review_text = models.TextField()
    star_rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )


class TopSellingProduct(BaseModel):
    product = models.ForeignKey(
        Product, related_name='top_selling_products', on_delete=models.CASCADE)
    total_revenue = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal('0'))
    sales_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return str(self.product)


@receiver(post_save, sender=Stock)
def update_top_selling_product_stats(sender, instance, **kwargs):
    if instance.event_type.name.lower() == 'sale':
        top_selling_product, created = TopSellingProduct.objects.get_or_create(
            product=instance.product)

        top_selling_product.sales_count += instance.quantity
        top_selling_product.total_revenue += Decimal(
            instance.product.price) * Decimal(instance.quantity)
        top_selling_product.save()

        if instance.product.is_top_seller:
            top_selling_product.is_top_seller = True
            top_selling_product.save()
    elif instance.event_type.name.lower() == 'refund':
        try:
            top_selling_product = TopSellingProduct.objects.get(
                product=instance.product)
            if top_selling_product.sales_count >= instance.quantity:
                top_selling_product.sales_count -= instance.quantity
                top_selling_product.total_revenue -= Decimal(
                    instance.product.price) * Decimal(instance.quantity)
                top_selling_product.save()

                if not instance.product.is_top_seller:
                    top_selling_product.is_top_seller = False
                    top_selling_product.save()
        except TopSellingProduct.DoesNotExist:
            pass
