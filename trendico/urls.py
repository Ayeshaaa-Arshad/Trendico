from django.urls import path
from trendico import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('get_products/<str:category>/',
         views.ProductsByCategoryView.as_view(), name='product-category'),
    path('store/<str:name>', views.StoreView.as_view(), name='store'),
    path('product/<str:name>', views.ProductView.as_view(), name='product'),
    path('checkout/', views.checkout, name='checkout'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name="logout"),
    path('register/', views.RegisterView.as_view(), name="register"),
    path('add_to_cart/', views.AddToCartView.as_view(), name="add_to_cart"),
    path('cart_summary/', views.CartSummaryView.as_view(), name='cart_summary'),
    path('remove_from_cart/<int:cart_item_id>/',
         views.RemoveFromCartView.as_view(), name='remove_from_cart'),
]
