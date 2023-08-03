from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from trendico.models import Product
from django.contrib.auth.forms import UserCreationForm
from trendico.forms import SignUpForm


# Create your views here.

class HomeView(View):
    def get(self,request):
        products=Product.objects.all()
        Product.is_new(products)
        Product.calculate_discount_percentage(products)
        return render(request,'index.html',{'Products':products})

def store(request):
    return render(request,'store.html')

def product(request):
    return render(request,'product.html')

def checkout(request):
    return render(request,'checkout.html')

class LoginView(View):
    def get(self,request):
        return render(request,'login.html')
    def post(self,request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully logged In")
            return redirect('home')
        else:
            messages.success(request, "Failed to log In")
            return redirect('login')

class LogoutView(View):
    def get(self,request):
        logout(request)
        messages.success(request,"Logged out")
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
        else:
            return render(request, self.template_name, {'form': form})

    def get(self, request):
        form = SignUpForm()
        return render(request, self.template_name, {'form': form})
