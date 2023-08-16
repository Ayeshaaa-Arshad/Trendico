from django.urls import path
from trendico import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('get_products/<str:category>/',
         views.ProductsByCategoryView.as_view(), name='product-category'),
    path('store/<str:name>', views.StoreView.as_view(), name='store'),
    path('product/<str:name>', views.ProductView.as_view(), name='product'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name="logout"),
    path('register/', views.RegisterView.as_view(), name="register"),
    path('cart/', views.CartView.as_view(), name="cart"),
    path('wishlist/<int:product_id>',
         views.WishlistView.as_view(), name="wishlist"),
    path('wishlist/', views.WishlistView.as_view(), name="wishlist"),
    path('remove_from_cart/<int:cart_item_id>/',
         views.RemoveFromCartView.as_view(), name='remove_from_cart'),
    path('remove_from_wishlist/<int:wishlist_item_id>/',
         views.RemoveFromWishlistView.as_view(), name='remove_from_wishlist'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
]
