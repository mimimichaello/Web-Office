from django import forms
from django.contrib import admin

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from django.utils.translation import gettext_lazy as _

from .models import ClientMore, CustomUser, Administrator, Manager, Employee, Client

class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'type')
    ordering = ('email',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'type')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

admin.site.register(CustomUser, UserAdmin)

admin.site.register(Administrator)

admin.site.register(Manager)

admin.site.register(Employee)


class ClientAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'company')
    readonly_fields = ('company',)

    def company(self, obj):
        return obj.client_more.company.name if obj.client_more else None


admin.site.register(Client, ClientAdmin)
