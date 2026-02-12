from django import forms
from .models import Order


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'phone', 'city', 'address', 'postal_code', 'notes']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Иван'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Иванов'}),
            'email': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'email@example.com'}),
            'phone': forms.TextInput(attrs={'class': 'form-input', 'placeholder': '+7 (999) 123-45-67'}),
            'city': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Москва'}),
            'address': forms.Textarea(attrs={'class': 'form-input', 'rows': 3, 'placeholder': 'Улица, дом, квартира'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-input', 'placeholder': '123456'}),
            'notes': forms.Textarea(attrs={'class': 'form-input', 'rows': 2, 'placeholder': 'Дополнительные пожелания'}),
        }
