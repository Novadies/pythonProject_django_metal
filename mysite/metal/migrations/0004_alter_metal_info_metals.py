# Generated by Django 4.2.3 on 2023-07-19 12:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('metal', '0003_remove_metal_class_chain_steel_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='metal_info',
            name='metals',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='metal.metal'),
        ),
    ]
