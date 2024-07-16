from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.shortcuts import get_object_or_404, redirect
from users.signals import update_company_code

from django.urls import reverse_lazy

from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin


from .models import Client, ClientMore, CustomUser
from companies.models import Company

from .forms import RegisterClientForm, LoginForm


class RegisterClientView(SuccessMessageMixin, CreateView):
    form_class = RegisterClientForm
    model = Client
    template_name = "users/register_client.html"
    extra_context = {"title": "Регистрация"}
    success_url = reverse_lazy("login")
    success_message = "Поздравляем!!!\nРегистрация прошла успешно."

    def form_valid(self, form):
        company_code = form.cleaned_data["company_code"]
        company = get_object_or_404(Company, unique_code=company_code)
        client = form.save(commit=False)
        client.save()
        client_more = ClientMore.objects.create(client=client, company=company)
        client_more.save()
        update_company_code(sender=self, instance=client, created=True)
        return super().form_valid(form)


class LoginView(SuccessMessageMixin, LoginView):
    """Login client"""

    form_class = LoginForm
    template_name = "users/login.html"
    extra_context = {"title": "LOGIN"}
    success_message = "Авторизация прошла успешно."

    def get_form(self, form_class=None):
        return self.form_class()

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                if user.type == CustomUser.Types.CLIENT:
                    return redirect("dashboard_client")
                else:
                    return redirect("dashboard")
        return render(request, self.template_name, {"form": form})
