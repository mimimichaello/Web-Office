from django.urls import path

from .views import (
    dashboard_client,
    DashboardView,
    CreateEmployeeView,
    CreateClientView,
    CreateCompanyView,
)

urlpatterns = [
    path("dashboard/", dashboard_client, name="dashboard_client"),
    path("admin-panel/", DashboardView.as_view(), name="dashboard"),
    path("create-employee/", CreateEmployeeView.as_view(), name="create_employee"),
    path("create-client/", CreateClientView.as_view(), name="create_client"),
    path("create-company/", CreateCompanyView.as_view(), name="create_company"),
]
