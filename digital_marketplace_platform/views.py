from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import CustomUserCreationForm
from .models import Product


def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # Redirect to home or another page
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to home or another page
        else:
            return render(request, 'registration/login.html', {'error': 'Invalid credentials'})
    return render(request, 'registration/login.html')

def user_logout(request):
    logout(request)
    return redirect('home')

def product_list(request):
    query = request.GET.get('q', '')
    filter_type = request.GET.get('type', '')

    # Filter products based on search query and type
    if query:
        products = Product.objects.filter(name__icontains=query)
    else:
        products = Product.objects.all()

    if filter_type:
        products = products.filter(type=filter_type)

    return render(request, 'product_list.html', {
        'products': products,
        'query': query,
        'filter_type': filter_type
    })