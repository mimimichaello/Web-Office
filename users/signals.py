from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Client
from companies.models import Company


@receiver(post_save, sender=Client)
def update_company_code(sender, instance, created, **kwargs):
    if created:
        if hasattr(instance, "more"):
            instance.more.company.unique_code = Company.generate_unique_code()
            instance.more.company.save()
