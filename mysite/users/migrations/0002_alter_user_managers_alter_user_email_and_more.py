# Generated by Django 4.2.3 on 2024-01-11 17:39

import django.contrib.auth.password_validation
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelManagers(
            name="user",
            managers=[],
        ),
        migrations.AlterField(
            model_name="user",
            name="email",
            field=models.EmailField(max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name="user",
            name="secret_login",
            field=models.CharField(max_length=128, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name="user",
            name="secret_password",
            field=models.CharField(
                max_length=128,
                null=True,
                validators=[
                    django.core.validators.MinLengthValidator(8),
                    django.contrib.auth.password_validation.validate_password,
                ],
            ),
        ),
    ]
