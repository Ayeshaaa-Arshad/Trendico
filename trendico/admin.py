from django.contrib import admin
from trendico.models import Product,ProductImage,ProductCategory,Stock
# Register your models here.

admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(ProductCategory)
admin.site.register(Stock)
