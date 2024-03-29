# Generated by Django 4.2.10 on 2024-03-07 17:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("user_registration", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="BillingStatement",
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
                ("billing_period", models.CharField(max_length=50)),
                ("statement_date", models.DateField()),
                ("due_date", models.DateField()),
                ("total_charges", models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    "payments_received",
                    models.DecimalField(decimal_places=2, max_digits=10),
                ),
                (
                    "outstanding_balance",
                    models.DecimalField(decimal_places=2, max_digits=10),
                ),
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
