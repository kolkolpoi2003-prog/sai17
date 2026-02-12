from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'email@example.com'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-input', 'placeholder': 'Имя пользователя'})
        self.fields['password1'].widget.attrs.update({'class': 'form-input', 'placeholder': 'Пароль'})
        self.fields['password2'].widget.attrs.update({'class': 'form-input', 'placeholder': 'Повторите пароль'})


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-input', 'placeholder': 'Имя пользователя'})
        self.fields['password'].widget.attrs.update({'class': 'form-input', 'placeholder': 'Пароль'})


class ProfileEditForm(forms.Form):
    first_name = forms.CharField(max_length=100, required=False,
                                  widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Имя'}))
    last_name = forms.CharField(max_length=100, required=False,
                                 widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Фамилия'}))
    email = forms.EmailField(required=False,
                              widget=forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Email'}))
    phone = forms.CharField(max_length=20, required=False,
                             widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Телефон'}))
    city = forms.CharField(max_length=100, required=False,
                            widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Город'}))
    address = forms.CharField(required=False,
                               widget=forms.Textarea(attrs={'class': 'form-input', 'rows': 3, 'placeholder': 'Адрес'}))
