from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Product


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'user_type')

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'availability_start', 'availability_end', 'type', 'allergens', 'image']
        widgets = {
            'availability_start': forms.DateInput(attrs={'type': 'date'}),
            'availability_end': forms.DateInput(attrs={'type': 'date'}),
        }
