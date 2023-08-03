from trendico import views
from django.urls import path

urlpatterns = [
    path('',views.HomeView.as_view(),name='home'),
    path('store/',views.store,name='store'),
    path('product/',views.product,name='product'),
    path('checkout/',views.checkout,name='checkout'),
    path('login/',views.LoginView.as_view(),name='login'),
    path('logout/', views.LogoutView.as_view(), name="logout"),
    path('register/', views.RegisterView.as_view(), name="register"),
]
