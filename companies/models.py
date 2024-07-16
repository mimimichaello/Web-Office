import random

from django.db import models

from django.utils.translation import gettext_lazy as _

class Company(models.Model):
    name = models.CharField(_('Company name'), max_length=100, help_text=_('Enter the company name'))
    address = models.CharField(_('Address'), max_length=255, help_text=_('Enter the company address'))
    contact_info = models.CharField(_('Contact info'), max_length=255, help_text=_('Enter the company contact info'))
    unique_code = models.CharField(_('Unique code'), max_length=6, unique=True, blank=True, null=True, help_text=_('Enter a unique code for the company'))


    class Meta:
        verbose_name = _('Company')
        verbose_name_plural = _('Companies')
    @classmethod
    def generate_unique_code(cls):
        while True:
            code = str(random.randint(100000, 999999))
            if not cls.objects.filter(unique_code=code).exists():
                return code

    def save(self, *args, **kwargs):
        if not self.unique_code:
            self.unique_code = self.generate_unique_code()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
