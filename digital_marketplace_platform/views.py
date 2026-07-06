from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from .forms import CustomUserCreationForm, ProductForm
from .models import Product, CartItem


def home(request):
    return render(request, 'home.html')

def pledge(request):
    return render(request, 'pledge.html')

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

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.user.is_authenticated:
        cart_item, created = CartItem.objects.get_or_create(
            user=request.user,
            product=product
        )
        if not created:
            cart_item.quantity += 1
            cart_item.save()
        return redirect('view_cart')
    else:
        return redirect('login')

def view_cart(request):
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
        total_price = sum(item.product.price * item.quantity for item in cart_items)
        return render(request, 'cart.html', {
            'cart_items': cart_items,
            'total_price': total_price
        })
    else:
        return redirect('login')

def product_management(request):
    if request.user.is_authenticated and request.user.user_type == 'producer':
        producer_products = Product.get_producer_products(request.user.id)
        return render(request, 'producer/product_management.html', {'products': producer_products})
    else:
        return redirect('home')

def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.producer = request.user
            product.save()
            return redirect('product_management')
    else:
        form = ProductForm()
    return render(request, 'producer/add_product.html', {'form': form})

def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.user == product.producer:
        if request.method == 'POST':
            form = ProductForm(request.POST, request.FILES, instance=product)
            if form.is_valid():
                form.save()
                return redirect('product_management')
        else:
            form = ProductForm(instance=product)
        return render(request, 'producer/edit_product.html', {'form': form})
    else:
        return redirect('home')

def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.user == product.producer:
        if request.method == 'POST':
            product.delete()
            return redirect('product_management')
        return render(request, 'producer/confirm_delete.html', {'product': product})
    else:
        return redirect('home')