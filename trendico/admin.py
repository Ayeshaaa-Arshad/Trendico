from django.contrib import admin
from trendico.models import Product, ProductImage, ProductCategory, Stock, TopSellingProduct, UserReview, EventType
# Register your models here.

admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(ProductCategory)
admin.site.register(Stock)
admin.site.register(TopSellingProduct)
admin.site.register(UserReview)
admin.site.register(EventType)
