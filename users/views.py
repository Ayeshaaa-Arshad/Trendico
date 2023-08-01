from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request,'index.html')

def store(request):
    return render(request,'store.html')

def product(request):
    return render(request,'product.html')

def checkout(request):
    return render(request,'checkout.html')


def login(request):
    return render(request,'login.html')