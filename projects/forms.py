from django import forms

from companies.models import Company
from users.models import Client, CustomUser

from django.contrib.auth.forms import UserCreationForm


class CreateEmployeeForm(forms.ModelForm):
    first_name = forms.CharField(
        label="Имя",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Имя"}),
    )
    last_name = forms.CharField(
        label="Фамилия",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Фамилия"}
        ),
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Email"}),
    )
    type = forms.ChoiceField(
        label="Тип",
        choices=CustomUser.Types.choices,
        widget=forms.Select(attrs={"class": "form-control"}),
        required=True,
    )
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Пароль"}
        ),
    )
    password_confirm = forms.CharField(
        label="Подтверждение пароля",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Подтверждение пароля"}
        ),
    )

    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name", "email", "type"]

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")
        if password != password_confirm:
            raise forms.ValidationError("Пароли не совпадают")
        return cleaned_data

    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name", "email", "type"]


class CreateClientForm(UserCreationForm):
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control text-dark", "placeholder": "Введите имя"}
        )
    )
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control text-dark", "placeholder": "Введите фамилию"}
        )
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={"class": "form-control text-dark", "placeholder": "Введите email"}
        )
    )
    company = forms.ModelChoiceField(
        queryset=Company.objects.all(),
        widget=forms.Select(attrs={"class": "form-control text-dark"}),
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control text-dark", "placeholder": "Введите пароль"}
        )
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control text-dark",
                "placeholder": "Подтвердите пароль",
            }
        )
    )

    class Meta:
        model = Client
        fields = (
            "first_name",
            "last_name",
            "email",
            "company",
            "password1",
            "password2",
        )


class CreateCompanyForm(forms.ModelForm):
    name = forms.CharField(
        label="Название компании",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Название компании"}
        ),
    )
    address = forms.CharField(
        label="Адрес",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Адрес"}),
    )
    contact_info = forms.CharField(
        label="Контактные данные",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Контактные данные"}
        ),
    )

    class Meta:
        model = Company
        fields = ("name", "address", "contact_info")
