from trendico import views
from django.urls import path

urlpatterns = [
    path('',views.home,name='home'),
    path('store/',views.store,name='store'),
    path('product/',views.product,name='product'),
    path('checkout/',views.checkout,name='checkout'),
    path('login/',views.login,name='login'),
]
