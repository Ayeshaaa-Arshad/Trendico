from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views import View
from django.core.paginator import Paginator
from django.db.models import Sum
from trendico.models import Product, ProductCategory
from trendico.forms import SignUpForm
from django.http import JsonResponse
import json
# Create your views here.


class HomeView(View):
    def get(self, request, category=None):
        categories = ProductCategory.objects.all()
        products = Product.objects.all()

        if category:
            products = Product.get_specific_products(category)

        products = products.annotate(
            remaining_quantity=Sum('stocks__quantity')
        )
        context = {
            'categories': categories,
            'Products': products,
            'selected_category': category
        }
        return render(request, 'index.html', context)


class ProductsByCategoryView(View):
    def get(self, request, category):
        products = Product.get_specific_products(category)

        products = products.annotate(
            remaining_quantity=Sum('stocks__quantity')
        )

        products_data = []
        for product in products:
            product_data = {
                'name': product.name,
                'price': product.price,
                'discount_price': product.discount_price,
                'category': product.category.name,
                'description': product.description,
                'image_url': product.images.first().image.url if product.images.first() else None,
                'is_new': product.is_new,
                'discount_percentage': product.discount_percentage,
            }
            products_data.append(product_data)

        return JsonResponse(products_data, safe=False)


class StoreView(View):
    template_name = 'store.html'

    def get(self, request, name):
        products = Product.get_specific_products(name)

        if products:
            products = products.annotate(
                remaining_quantity=Sum('stocks__quantity')
            )
            request.session['selected_category'] = name
            paginator = Paginator(products, 6)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            return render(request, self.template_name, {'page_obj': page_obj})
        messages.success(request, "No Product Available")
        return redirect('home')


def product(request):
    return render(request, 'product.html')


def checkout(request):
    return render(request, 'checkout.html')


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully logged In")
            return redirect('home')
        messages.success(request, "Failed to log In")
        return redirect('login')


class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, "Logged out")
        return redirect('home')


class RegisterView(View):
    template_name = 'login.html'

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "Successfully Registered")
            return redirect('home')
        return render(request, self.template_name, {'form': form})

    def get(self, request):
        form = SignUpForm()
        return render(request, self.template_name, {'form': form})
