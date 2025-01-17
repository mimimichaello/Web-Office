# Generated by Django 4.2 on 2024-07-14 19:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("users", "0002_alter_clientmore_client"),
        ("companies", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Project",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=200)),
                (
                    "company",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="companies.company",
                        verbose_name="Компания",
                    ),
                ),
                (
                    "project_manager",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="users.manager",
                        verbose_name="Responsible for the project",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Task",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("description", models.TextField(blank=True, null=True)),
                (
                    "project",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="projects.project",
                        verbose_name="Проект",
                    ),
                ),
                (
                    "task_executor",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="users.employee",
                        verbose_name="Responsible for the task",
                    ),
                ),
            ],
        ),
    ]
