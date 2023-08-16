from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views import View
from django.core.paginator import Paginator
from trendico.models import Product, ProductCategory, Cart, CartItem, Wishlist
from trendico.forms import SignUpForm, OrderForm
from django.http import JsonResponse
from trendico.tasks import send_order_notification_email

# Create your views here.
class HomeView(View):
    def get(self, request, category=None):
        categories = ProductCategory.objects.all()
        products = Product.objects.all()

        if category:
            products = Product.get_specific_products(category)

        context = {
            'categories': categories,
            'Products': products,
            'selected_category': category
        }
        return render(request, 'index.html', context)


class ProductsByCategoryView(View):
    def get(self, request, category):
        products = Product.get_specific_products(category)

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
            request.session['selected_category'] = name
            paginator = Paginator(products, 6)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            return render(request, self.template_name, {'page_obj': page_obj})
        messages.success(request, "No Product Available")
        return redirect('home')


class ProductView(View):
    template_name = 'product.html'

    def get(self, request, name):
        try:
            product = Product.objects.get(name=name)
            context = {'product': product}
            return render(request, self.template_name, context)
        except Product.DoesNotExist:
            return redirect('home')


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


class CartView(LoginRequiredMixin, View):
    login_url = 'login.html'

    def get(self, request):
        cart = Cart.objects.filter(user=request.user).first()
        if cart:
            cart_item_count = cart.cart_items.count()
            return JsonResponse({'cart_item_count': cart_item_count, 'cart_total': cart.cart_total})
        return JsonResponse({'cart_item_count': 0, 'cart_total': 0})

    def post(self, request):
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))

        product = Product.objects.get(pk=product_id)

        cart, _ = Cart.objects.get_or_create(user=request.user)

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart, product=product)

        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        else:
            cart_item.quantity = quantity
            cart_item.save()

        messages.success(
            request, f"{quantity} {product.name}(s) added to your cart.")
        return redirect('home')

    def handle_no_permission(self):
        messages.error(self.request, "You need to log in to access this page.")
        return redirect('login')


class RemoveFromCartView(LoginRequiredMixin, View):
    def post(self, request, cart_item_id):
        try:
            cart_item = CartItem.objects.get(
                id=cart_item_id, cart__user=request.user)
            cart_item.delete()
            cart_item_count = CartItem.objects.filter(
                cart__user=request.user).count()
            return JsonResponse({'success': True, 'cart_item_count': cart_item_count})
        except CartItem.DoesNotExist:
            return JsonResponse({'success': False})

    def handle_no_permission(self):
        messages.error(self.request, "You need to log in to access this page.")
        return redirect('login')


class WishlistView(LoginRequiredMixin, View):
    def post(self, request, product_id):
        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            return JsonResponse({'error': 'Product not found'}, status=400)

        wishlist, _ = Wishlist.objects.get_or_create(user=request.user)
        wishlist.items.add(product)

        messages.success(request, f"{product.name}(s) added to your wishlist.")

        wishlist_item_count = wishlist.items.count()

        return JsonResponse({
            'success': True,
            'message': f"{product.name}(s) added to your wishlist.",
            'wishlist_item_count': wishlist_item_count,
        })


class RemoveFromWishlistView(LoginRequiredMixin, View):
    def post(self, request, wishlist_item_id):
        try:
            wishlist = Wishlist.objects.get(user=request.user)
            product = wishlist.items.get(pk=wishlist_item_id)
            wishlist.items.remove(product)

            message = f"{product.name}(s) removed from your wishlist."
            success = True
        except Wishlist.DoesNotExist:
            message = "Wishlist not found."
            success = False
        except Product.DoesNotExist:
            message = "Product not found in wishlist."
            success = False

        wishlist_item_count = wishlist.items.count()

        return JsonResponse({'success': success, 'message': message, 'wishlist_item_count': wishlist_item_count})

    def get(self, request):
        wishlist = Wishlist.objects.get_or_create(user=request.user)[0]
        wishlist_items = wishlist.items.all()

        wishlist_data = []
        for item in wishlist_items:
            wishlist_data.append({
                'id': item.id,
                'name': item.name,
                'price': item.price,
                'image_url': item.images.first().image.url,
            })

        return JsonResponse({
            'wishlist_item_count': wishlist_items.count(),
            'wishlist_items': wishlist_data,
        })


class CheckoutView(View):
    template_name = 'checkout.html'

    def get(self, request, *args, **kwargs):
        form = OrderForm()
        cart = Cart.objects.get(user=request.user)
        item_totals = [cart_item.quantity * cart_item.product.price for cart_item in cart.cart_items.all()]
        context = {
            'form': form,
            'cart_items': cart.cart_items.all(),
            'cart': cart,
            'item_totals': item_totals,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()

            cart = Cart.objects.get(user=request.user)
            selected_item_ids = request.POST.getlist('selected_items')

            if selected_item_ids:
                selected_cart_items = cart.cart_items.filter(id__in=selected_item_ids)

                order.products.set([item.product.id for item in selected_cart_items])

                selected_cart_items.delete()

                order.save()

                send_order_notification_email.delay(order.id)

                messages.success(request, "Your Order is placed ")
                return redirect('home')

        cart = Cart.objects.get(user=request.user)
        item_totals = [cart_item.quantity * cart_item.product.price for cart_item in cart.cart_items.all()]
        context = {
            'form': form,
            'cart_items': cart.cart_items.all(),
            'cart': cart,
            'item_totals': item_totals,
        }
        return render(request, self.template_name, context)
