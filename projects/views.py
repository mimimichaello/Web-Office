from django.shortcuts import render

from django.urls import reverse_lazy

from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin

from .models import Project, Task
from companies.models import Company
from users.models import Client, ClientMore, CustomUser, Manager, Employee

from .forms import CreateClientForm, CreateCompanyForm, CreateEmployeeForm

from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView,
)


def dashboard_client(request):
    client = Client.objects.get(id=request.user.id)
    company = client.more.company
    projects = Project.objects.filter(company=company)
    tasks = Task.objects.filter(project__in=projects)

    context = {
        "title": "Dashboard",
        "client": client,
        "projects": projects,
        "tasks": tasks,
        "company": company,
    }
    return render(request, "projects/dashboard_client.html", context)


class DashboardView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Task
    template_name = "projects/dashboard.html"
    context_object_name = "tasks"

    def test_func(self):
        user = self.request.user
        required_groups = ["Administrator", "Employee", "Manager"]
        return any(group.name in required_groups for group in user.groups.all())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context["title"] = "Admin Panel"
        context["user"] = user
        context["clients"] = Client.objects.all()
        context["managers"] = Manager.objects.all()
        context["employees"] = Employee.objects.all()
        context["projects"] = Project.objects.all()
        context["companies"] = Company.objects.all()
        context["employee_task"] = Task.objects.filter(task_executor=user)
        return context


class CreateEmployeeView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = CustomUser
    form_class = CreateEmployeeForm
    success_url = reverse_lazy("dashboard")
    template_name = "projects/create_employee.html"
    extra_context = {"title": "Добавить сотрудника"}

    def test_func(self):
        return self.request.user.groups.filter(name="Administrator").exists()

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data["password"])
        user.save()
        return super().form_valid(form)


class CreateClientView(LoginRequiredMixin,UserPassesTestMixin, CreateView):
    model = Client
    form_class = CreateClientForm
    success_url = reverse_lazy("dashboard")
    template_name = "projects/create_client.html"
    extra_context = {"title": "Добавить клиента"}

    context_object_name = "companies"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["companies"] = Company.objects.all()
        print(context["companies"])
        return context


    def test_func(self):
        user = self.request.user
        required_groups = ["Administrator", "Manager"]
        return any(group.name in required_groups for group in user.groups.all())

    def form_valid(self, form):
        client = form.save(commit=False)
        company = form.cleaned_data['company']
        client.company = company
        client.save()
        client_more = ClientMore(client=client, company=company)
        client_more.save()
        return super().form_valid(form)



class CreateCompanyView(LoginRequiredMixin,UserPassesTestMixin, CreateView):
    model = Company
    form_class = CreateCompanyForm
    success_url = reverse_lazy("dashboard")
    template_name = "projects/create_company.html"
    extra_context = {"title": "Добавить компанию"}

    def test_func(self):
        user = self.request.user
        required_groups = ["Administrator", "Manager"]
        return any(group.name in required_groups for group in user.groups.all())

    def form_valid(self, form):
        company = form.save(commit=False)
        company.save()
        return super().form_valid(form)
