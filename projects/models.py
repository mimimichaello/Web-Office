from django.db import models

from users.models import Administrator, Manager, Employee, Client
from companies.models import Company

class Project(models.Model):
    name = models.CharField(max_length=200)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name='Компания')
    project_manager = models.ForeignKey(Manager, on_delete=models.SET_NULL, null=True, verbose_name='Responsible for the project')

    def __str__(self):
        return f'{self.name} - {self.project_manager}'


class Task(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name='Проект')
    task_executor = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, verbose_name='Responsible for the task')

    def __str__(self):
        return f'{self.name} - {self.task_executor}'
