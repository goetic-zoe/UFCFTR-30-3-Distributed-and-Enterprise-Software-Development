import requests
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from .forms import CustomUserCreationForm, ProductForm
from .models import Product, CartItem, Order, OrderItem
import json
import uuid

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

def checkout(request):
    if request.user.is_authenticated:
        return render(request, 'checkout.html')
    else:
        return redirect('login')

def create_order(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            delivery_address = data.get('delivery_address')
            postcode = data.get('postcode')

            # Calculate total amount
            cart_items = CartItem.objects.filter(user=request.user)
            total_amount = sum(item.product.price * item.quantity for item in cart_items)

            # Create order
            order_id = uuid.uuid4().hex  # Generate a unique order ID
            order = Order.objects.create(
                customer=request.user,
                total_amount=total_amount,
                delivery_address=delivery_address,
                postcode=postcode,
                status='pending'
            )

            # Create order items
            for item in cart_items:
                OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity)

            # Create PayPal order (server-side)
            paypal_client_id = request.settings.PAYPAL_CLIENT_ID
            paypal_secret_id = request.settings.PAYPAL_SECRET_ID

            auth_response = requests.post(
                'https://api.sandbox.paypal.com/v1/oauth2/token',
                headers={'Accept': 'application/json', 'Accept-Language': 'en_US'},
                data={
                    'grant_type': 'client_credentials'
                },
                auth=(paypal_client_id, paypal_secret_id)
            )
            access_token = auth_response.json().get('access_token')

            order_create_url = 'https://api-m.sandbox.paypal.com/v2/checkout/orders'
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {access_token}'
            }
            body = {
                "intent": "CAPTURE",
                "purchase_units": [{
                    "amount": {
                        "currency_code": "GBP",
                        "value": str(total_amount)
                    }
                }],
                "application_context": {
                    "brand_name": "BRFN Marketplace",
                    "landing_page": "BILLING",
                    "user_action": "PAY_NOW",
                    "return_url": "https://example.com/your-approve-url",  # Replace with your return URL
                    "cancel_url": "https://example.com/your-cancel-url"    # Replace with your cancel URL
                }
            }

            response = requests.post(order_create_url, headers=headers, json=body)
            order_response_data = response.json()

            if 'id' in order_response_data:
                return JsonResponse({'orderId': order_response_data['id']})
            else:
                print(f"Error creating PayPal order: {order_response_data}")
                return JsonResponse({'error': 'Failed to create PayPal order'}, status=500)
        except Exception as e:
            print(f"Error creating order: {e}")
            return JsonResponse({'error': 'Failed to create order'}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

def capture_order(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            paypal_order_id = data.get('orderId')

            # Capture PayPal order (server-side)
            paypal_client_id = request.settings.PAYPAL_CLIENT_ID
            paypal_secret_id = request.settings.PAYPAL_SECRET_ID

            auth_response = requests.post(
                'https://api.sandbox.paypal.com/v1/oauth2/token',
                headers={'Accept': 'application/json', 'Accept-Language': 'en_US'},
                data={
                    'grant_type': 'client_credentials'
                },
                auth=(paypal_client_id, paypal_secret_id)
            )
            access_token = auth_response.json().get('access_token')

            capture_url = f'https://api-m.sandbox.paypal.com/v2/checkout/orders/{paypal_order_id}/capture'
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {access_token}'
            }

            response = requests.post(capture_url, headers=headers)
            capture_response_data = response.json()

            if capture_response_data.get('status') == 'COMPLETED':
                # Update order status to confirm
                local_order = Order.objects.filter(order_id=paypal_order_id).first()
                if local_order:
                    local_order.status = 'confirmed'
                    local_order.save()
                return JsonResponse({'status': 'COMPLETED'})
            else:
                print(f"Error capturing PayPal order: {capture_response_data}")
                return JsonResponse({'error': 'Failed to capture PayPal order'}, status=500)
        except Exception as e:
            print(f"Error capturing order: {e}")
            return JsonResponse({'error': 'Failed to capture order'}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=405)