from django.urls import path
from trendico import views

urlpatterns = [
    path('',views.HomeView.as_view(),name='home'),
    path('get_products/<str:category>/', views.ProductsByCategoryView.as_view(), name='product-category'),
    path('store/<str:name>',views.StoreView.as_view(),name='store'),
    path('product/',views.product,name='product'),
    path('checkout/',views.checkout,name='checkout'),
    path('login/',views.LoginView.as_view(),name='login'),
    path('logout/', views.LogoutView.as_view(), name="logout"),
    path('register/', views.RegisterView.as_view(), name="register"),
]
