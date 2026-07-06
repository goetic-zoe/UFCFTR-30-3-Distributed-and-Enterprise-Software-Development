"""
URL configuration for bristol_regional_food_network project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another Urlconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from digital_marketplace_platform.views import home, register, user_login, user_logout, product_list, add_to_cart, \
    view_cart, pledge, product_management, add_product, edit_product, delete_product

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('products/', product_list, name='product_list'),
    path('add_to_cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/', view_cart, name='view_cart'),
    path('pledge', pledge, name='pledge'),
    path('product-management/', product_management, name='product_management'),
    path('add-product/', add_product, name='add_product'),
    path('edit-product/<int:product_id>/', edit_product, name='edit_product'),
    path('delete-product/<int:product_id>/', delete_product, name='delete_product'),
]
