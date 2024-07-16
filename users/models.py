from django.utils import timezone

from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _

from companies.models import Company
from users.managers import UserManager

from django.contrib.auth.models import Group


class CustomUser(AbstractBaseUser, PermissionsMixin):

    class Types(models.TextChoices):
        ADMINISTRATOR = "ADMINISTRATOR", "Administrator"
        MANAGER = "MANAGER", "Manager"
        EMPLOYEE = "EMPLOYEE", "Employee"
        CLIENT = "CLIENT", "Client"

    base_type = Types.CLIENT

    # What type of user are we?
    type = models.CharField(
        _("Type"), max_length=50, choices=Types.choices, default=base_type
    )

    email = models.EmailField(_("Email"), unique=True)

    first_name = models.CharField(_("first name"), max_length=100)
    last_name = models.CharField(_("last name"), max_length=100)

    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )

    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_("Designates whether this user should be treated as active."),
    )

    groups = models.ManyToManyField(
        Group,
        verbose_name=_("группы"),
        blank=True,
        help_text=_("Группы, к которым принадлежит пользователь. Пользователь получит все разрешения, предоставленные каждой из его групп."),
        related_name="user_set",
        related_query_name="user",
    )

    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = "email"

    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)


class AdministratorManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return (
            super()
            .get_queryset(*args, **kwargs)
            .filter(type=CustomUser.Types.ADMINISTRATOR)
        )


class ManagerManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return (
            super().get_queryset(*args, **kwargs).filter(type=CustomUser.Types.MANAGER)
        )


class EmployeeManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return (
            super().get_queryset(*args, **kwargs).filter(type=CustomUser.Types.EMPLOYEE)
        )


class ClientManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return (
            super().get_queryset(*args, **kwargs)
           .filter(type=CustomUser.Types.CLIENT)
           .select_related('client_more__company')
        )


class Administrator(CustomUser):
    base_type = CustomUser.Types.ADMINISTRATOR
    objects = AdministratorManager()

    class Meta:
        proxy = True


class Manager(CustomUser):
    base_type = CustomUser.Types.MANAGER
    objects = ManagerManager()

    class Meta:
        proxy = True


class Employee(CustomUser):
    base_type = CustomUser.Types.EMPLOYEE
    objects = EmployeeManager()

    class Meta:
        proxy = True



class Client(CustomUser):
    base_type = CustomUser.Types.CLIENT
    objects = ClientManager()

    @property
    def more(self):
        return self.client_more

    class Meta:
        proxy = True


class ClientMore(models.Model):
    client = models.OneToOneField(Client, on_delete=models.CASCADE, related_name='client_more')
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
