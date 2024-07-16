from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group

from users.models import CustomUser


@receiver(post_save, sender=CustomUser)
def assign_group(sender, instance, created, **kwargs):
    if created:
        if instance.type == CustomUser.Types.ADMINISTRATOR:
            group = Group.objects.get(name='Administrator')
        elif instance.type == CustomUser.Types.MANAGER:
            group = Group.objects.get(name='Manager')
        elif instance.type == CustomUser.Types.EMPLOYEE:
            group = Group.objects.get(name='Employee')
        instance.groups.add(group)
