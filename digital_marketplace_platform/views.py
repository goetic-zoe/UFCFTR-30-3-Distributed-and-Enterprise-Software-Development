from django.shortcuts import render
from .models import Product

def home(request):
    return render(request, 'home.html')