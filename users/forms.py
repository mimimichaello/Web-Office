from django import forms
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate

from .models import Client

class RegisterClientForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control text-dark', 'placeholder': 'Введите имя'
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control text-dark', 'placeholder': 'Введите фамилию'
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control text-dark', 'placeholder': 'Введите email'
    }))
    company_code = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control text-dark', 'placeholder': 'Введите код компании'
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control text-dark', 'placeholder': 'Введите пароль'
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control text-dark', 'placeholder': 'Подтвердите пароль'
    }))

    class Meta:
        model = Client
        fields = ('first_name', 'last_name', 'email', 'company_code', 'password1', 'password2')


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control text-dark', 'placeholder': 'Email'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control text-dark', 'placeholder': 'Password'
    }))

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        user = authenticate(email=email, password=password)
        if not user:
            raise forms.ValidationError('Неверный электронный адрес или пароль')
        return self.cleaned_data
