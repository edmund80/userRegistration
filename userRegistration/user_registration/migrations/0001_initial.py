# Generated by Django 4.2.10 on 2024-02-23 16:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="PatientProfile",
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
                ("image", models.ImageField(upload_to="images")),
                ("first_name", models.CharField(null=True)),
                ("last_name", models.CharField(null=True)),
                ("address", models.CharField(null=True)),
                ("city", models.CharField(null=True)),
                ("state", models.CharField(null=True)),
                ("zip", models.CharField(null=True)),
                ("phone", models.CharField(null=True)),
                ("email", models.EmailField(max_length=254, null=True)),
                ("medications", models.CharField(null=True)),
                ("diagnosis", models.CharField(null=True)),
                ("insurance_card", models.ImageField(null=True, upload_to="images")),
                ("id_card", models.ImageField(null=True, upload_to="images")),
                ("next_of_kin_name", models.CharField(null=True)),
                ("next_of_kin_number", models.CharField(null=True)),
                ("text_billing_reminder", models.BooleanField(null=True)),
                ("email_billing_reminder", models.BooleanField(null=True)),
                ("text_appointment_reminder", models.BooleanField(null=True)),
                ("email_appointment_reminder", models.BooleanField(null=True)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="EmployeeProfile",
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
                ("image", models.ImageField(null=True, upload_to="images")),
                ("first_name", models.CharField(null=True)),
                ("last_name", models.CharField(null=True)),
                ("address", models.CharField(null=True)),
                ("city", models.CharField(null=True)),
                ("state", models.CharField(null=True)),
                ("zip", models.CharField(null=True)),
                ("phone", models.CharField(null=True)),
                ("email", models.EmailField(max_length=254, null=True)),
                ("supervisor", models.BooleanField(null=True)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="BillingReminder",
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
                ("message", models.TextField()),
                ("send_datetime", models.DateTimeField()),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]