from django.contrib import admin
from trendico.models import Product, ProductImage, ProductCategory, Stock, TopSellingProduct, UserReview
# Register your models here.

admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(ProductCategory)
admin.site.register(Stock)
admin.site.register(TopSellingProduct)
admin.site.register(UserReview)
