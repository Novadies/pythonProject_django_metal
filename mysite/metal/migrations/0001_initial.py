# Generated by Django 4.2.3 on 2023-11-19 16:07

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
            name="Metal",
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
                (
                    "C",
                    models.CharField(
                        blank=True, max_length=20, verbose_name="Элемент C"
                    ),
                ),
                (
                    "Si",
                    models.CharField(
                        blank=True, max_length=20, verbose_name="Элемент Si"
                    ),
                ),
                (
                    "Mn",
                    models.CharField(
                        blank=True, max_length=20, verbose_name="Элемент Mn"
                    ),
                ),
                (
                    "Cr",
                    models.CharField(
                        blank=True, max_length=20, verbose_name="Элемент Cr"
                    ),
                ),
                (
                    "Ni",
                    models.CharField(
                        blank=True, max_length=20, verbose_name="Элемент Ni"
                    ),
                ),
                (
                    "Ti",
                    models.CharField(
                        blank=True, max_length=20, verbose_name="Элемент Ti"
                    ),
                ),
                (
                    "Al",
                    models.CharField(
                        blank=True, max_length=20, verbose_name="Элемент Al"
                    ),
                ),
                (
                    "W",
                    models.CharField(
                        blank=True, max_length=20, verbose_name="Элемент W"
                    ),
                ),
                (
                    "Mo",
                    models.CharField(
                        blank=True, max_length=20, verbose_name="Элемент Mo"
                    ),
                ),
                (
                    "Nb",
                    models.CharField(
                        blank=True, max_length=20, verbose_name="Элемент Nb"
                    ),
                ),
                (
                    "V",
                    models.CharField(
                        blank=True, max_length=20, verbose_name="Элемент V"
                    ),
                ),
                (
                    "S",
                    models.CharField(
                        blank=True, max_length=20, verbose_name="Элемент S"
                    ),
                ),
                (
                    "P",
                    models.CharField(
                        blank=True, max_length=20, verbose_name="Элемент P"
                    ),
                ),
                (
                    "Cu",
                    models.CharField(
                        blank=True, max_length=20, verbose_name="Элемент Cu"
                    ),
                ),
                (
                    "Co",
                    models.CharField(
                        blank=True, max_length=20, verbose_name="Элемент Co"
                    ),
                ),
                (
                    "Zr",
                    models.CharField(
                        blank=True, max_length=20, verbose_name="Элемент Zr"
                    ),
                ),
                (
                    "Be",
                    models.CharField(
                        blank=True, max_length=20, verbose_name="Элемент Be"
                    ),
                ),
                (
                    "Se",
                    models.CharField(
                        blank=True, max_length=20, verbose_name="Элемент Se"
                    ),
                ),
                (
                    "N",
                    models.CharField(
                        blank=True, max_length=20, verbose_name="Элемент N"
                    ),
                ),
                (
                    "Pb",
                    models.CharField(
                        blank=True, max_length=20, verbose_name="Элемент Pb"
                    ),
                ),
                (
                    "Fe",
                    models.CharField(
                        blank=True, max_length=20, verbose_name="Элемент Fe"
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Metal_2",
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
                (
                    "C_min",
                    models.FloatField(
                        blank=True,
                        db_index=True,
                        null=True,
                        verbose_name="Минимум элемента C_min",
                    ),
                ),
                (
                    "C_max",
                    models.FloatField(
                        blank=True,
                        db_index=True,
                        null=True,
                        verbose_name="Максимум элемента C_max",
                    ),
                ),
                (
                    "Si_min",
                    models.FloatField(
                        blank=True,
                        db_index=True,
                        null=True,
                        verbose_name="Минимум элемента Si_min",
                    ),
                ),
                (
                    "Si_max",
                    models.FloatField(
                        blank=True,
                        db_index=True,
                        null=True,
                        verbose_name="Максимум элемента Si_max",
                    ),
                ),
                (
                    "Mn_min",
                    models.FloatField(
                        blank=True,
                        db_index=True,
                        null=True,
                        verbose_name="Минимум элемента Mn_min",
                    ),
                ),
                (
                    "Mn_max",
                    models.FloatField(
                        blank=True,
                        db_index=True,
                        null=True,
                        verbose_name="Максимум элемента Mn_max",
                    ),
                ),
                (
                    "Cr_min",
                    models.FloatField(
                        blank=True,
                        db_index=True,
                        null=True,
                        verbose_name="Минимум элемента Cr_min",
                    ),
                ),
                (
                    "Cr_max",
                    models.FloatField(
                        blank=True,
                        db_index=True,
                        null=True,
                        verbose_name="Максимум элемента Cr_max",
                    ),
                ),
                (
                    "Ni_min",
                    models.FloatField(
                        blank=True,
                        db_index=True,
                        null=True,
                        verbose_name="Минимум элемента Ni_min",
                    ),
                ),
                (
                    "Ni_max",
                    models.FloatField(
                        blank=True,
                        db_index=True,
                        null=True,
                        verbose_name="Максимум элемента Ni_max",
                    ),
                ),
                (
                    "Ti_min",
                    models.FloatField(
                        blank=True,
                        db_index=True,
                        null=True,
                        verbose_name="Минимум элемента Ti_min",
                    ),
                ),
                (
                    "Ti_max",
                    models.FloatField(
                        blank=True,
                        db_index=True,
                        null=True,
                        verbose_name="Максимум элемента Ti_max",
                    ),
                ),
                (
                    "Al_min",
                    models.FloatField(
                        blank=True,
                        db_index=True,
                        null=True,
                        verbose_name="Минимум элемента Al_min",
                    ),
                ),
                (
                    "Al_max",
                    models.FloatField(
                        blank=True,
                        db_index=True,
                        null=True,
                        verbose_name="Максимум элемента Al_max",
                    ),
                ),
                (
                    "W_min",
                    models.FloatField(
                        blank=True,
                        db_index=True,
                        null=True,
                        verbose_name="Минимум элемента W_min",
                    ),
                ),
                (
                    "W_max",
                    models.FloatField(
                        blank=True,
                        db_index=True,
                        null=True,
                        verbose_name="Максимум элемента W_max",
                    ),
                ),
                (
                    "Mo_min",
                    models.FloatField(
                        blank=True,
                        db_index=True,
                        null=True,
                        verbose_name="Минимум элемента Mo_min",
                    ),
                ),
                (
                    "Mo_max",
                    models.FloatField(
                        blank=True,
                        db_index=True,
                        null=True,
                        verbose_name="Максимум элемента Mo_max",
                    ),
                ),
                (
                    "Nb_min",
                    models.FloatField(
                        blank=True,
                        db_index=True,
                        null=True,
                        verbose_name="Минимум элемента Nb_min",
                    ),
                ),
                (
                    "Nb_max",
                    models.FloatField(
                        blank=True,
                        db_index=True,
                        null=True,
                        verbose_name="Максимум элемента Nb_max",
                    ),
                ),
                (
                    "V_min",
                    models.FloatField(
                        blank=True,
                        db_index=True,
                        null=True,
                        verbose_name="Минимум элемента V_min",
                    ),
                ),
                (
                    "V_max",
                    models.FloatField(
                        blank=True,
                        db_index=True,
                        null=True,
                        verbose_name="Максимум элемента V_max",
                    ),
                ),
                (
                    "S_min",
                    models.FloatField(
                        blank=True,
                        db_index=True,
                        null=True,
                        verbose_name="Минимум элемента S_min",
                    ),
                ),
                (
                    "S_max",
                    models.FloatField(
                        blank=True,
                        db_index=True,
                        null=True,
                        verbose_name="Максимум элемента S_max",
                    ),
                ),
                (
                    "P_min",
                    models.FloatField(
                        blank=True,
                        db_index=True,
                        null=True,
                        verbose_name="Минимум элемента P_min",
                    ),
                ),
                (
                    "P_max",
                    models.FloatField(
                        blank=True,
                        db_index=True,
                        null=True,
                        verbose_name="Максимум элемента P_max",
                    ),
                ),
                (
                    "Cu_min",
                    models.FloatField(
                        blank=True,
                        db_index=True,
                        null=True,
                        verbose_name="Минимум элемента Cu_min",
                    ),
                ),
                (
                    "Cu_max",
                    models.FloatField(
                        blank=True,
                        db_index=True,
                        null=True,
                        verbose_name="Максимум элемента Cu_max",
                    ),
                ),
                (
                    "Co_min",
                    models.FloatField(
                        blank=True,
                        db_index=True,
                        null=True,
                        verbose_name="Минимум элемента Co_min",
                    ),
                ),
                (
                    "Co_max",
                    models.FloatField(
                        blank=True,
                        db_index=True,
                        null=True,
                        verbose_name="Максимум элемента Co_max",
                    ),
                ),
                (
                    "Zr_min",
                    models.FloatField(
                        blank=True,
                        db_index=True,
                        null=True,
                        verbose_name="Минимум элемента Zr_min",
                    ),
                ),
                (
                    "Zr_max",
                    models.FloatField(
                        blank=True,
                        db_index=True,
                        null=True,
                        verbose_name="Максимум элемента Zr_max",
                    ),
                ),
                (
                    "Be_min",
                    models.FloatField(
                        blank=True,
                        db_index=True,
                        null=True,
                        verbose_name="Минимум элемента Be_min",
                    ),
                ),
                (
                    "Be_max",
                    models.FloatField(
                        blank=True,
                        db_index=True,
                        null=True,
                        verbose_name="Максимум элемента Be_max",
                    ),
                ),
                (
                    "Se_min",
                    models.FloatField(
                        blank=True,
                        db_index=True,
                        null=True,
                        verbose_name="Минимум элемента Se_min",
                    ),
                ),
                (
                    "Se_max",
                    models.FloatField(
                        blank=True,
                        db_index=True,
                        null=True,
                        verbose_name="Максимум элемента Se_max",
                    ),
                ),
                (
                    "N_min",
                    models.FloatField(
                        blank=True,
                        db_index=True,
                        null=True,
                        verbose_name="Минимум элемента N_min",
                    ),
                ),
                (
                    "N_max",
                    models.FloatField(
                        blank=True,
                        db_index=True,
                        null=True,
                        verbose_name="Максимум элемента N_max",
                    ),
                ),
                (
                    "Pb_min",
                    models.FloatField(
                        blank=True,
                        db_index=True,
                        null=True,
                        verbose_name="Минимум элемента Pb_min",
                    ),
                ),
                (
                    "Pb_max",
                    models.FloatField(
                        blank=True,
                        db_index=True,
                        null=True,
                        verbose_name="Максимум элемента Pb_max",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Metal_class",
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
                (
                    "steel_class",
                    models.CharField(
                        blank=True,
                        max_length=99,
                        unique=True,
                        verbose_name="Класс стали",
                    ),
                ),
                (
                    "slug",
                    models.SlugField(
                        blank=True, max_length=100, null=True, unique=True
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Metal_info",
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
                ("steel", models.CharField(blank=True, max_length=50)),
                (
                    "steel_info",
                    models.TextField(blank=True, verbose_name="Информация по стали"),
                ),
                (
                    "slug",
                    models.SlugField(
                        blank=True, max_length=100, null=True, unique=True
                    ),
                ),
                (
                    "metals",
                    models.OneToOneField(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="metal.metal",
                    ),
                ),
                (
                    "metals_class",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="metals_info",
                        to="metal.metal_class",
                    ),
                ),
            ],
            options={
                "verbose_name": "Информация по сплавам",
                "verbose_name_plural": "Информация по сплавам (список)",
                "ordering": ["steel"],
            },
        ),
        migrations.CreateModel(
            name="MetalSearch",
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
                (
                    "C",
                    models.CharField(
                        blank=True, max_length=20, verbose_name="Элемент C"
                    ),
                ),
                (
                    "Si",
                    models.CharField(
                        blank=True, max_length=20, verbose_name="Элемент Si"
                    ),
                ),
                (
                    "Mn",
                    models.CharField(
                        blank=True, max_length=20, verbose_name="Элемент Mn"
                    ),
                ),
                (
                    "Cr",
                    models.CharField(
                        blank=True, max_length=20, verbose_name="Элемент Cr"
                    ),
                ),
                (
                    "Ni",
                    models.CharField(
                        blank=True, max_length=20, verbose_name="Элемент Ni"
                    ),
                ),
                (
                    "Ti",
                    models.CharField(
                        blank=True, max_length=20, verbose_name="Элемент Ti"
                    ),
                ),
                (
                    "Al",
                    models.CharField(
                        blank=True, max_length=20, verbose_name="Элемент Al"
                    ),
                ),
                (
                    "W",
                    models.CharField(
                        blank=True, max_length=20, verbose_name="Элемент W"
                    ),
                ),
                (
                    "Mo",
                    models.CharField(
                        blank=True, max_length=20, verbose_name="Элемент Mo"
                    ),
                ),
                (
                    "Nb",
                    models.CharField(
                        blank=True, max_length=20, verbose_name="Элемент Nb"
                    ),
                ),
                (
                    "V",
                    models.CharField(
                        blank=True, max_length=20, verbose_name="Элемент V"
                    ),
                ),
                (
                    "S",
                    models.CharField(
                        blank=True, max_length=20, verbose_name="Элемент S"
                    ),
                ),
                (
                    "P",
                    models.CharField(
                        blank=True, max_length=20, verbose_name="Элемент P"
                    ),
                ),
                (
                    "Cu",
                    models.CharField(
                        blank=True, max_length=20, verbose_name="Элемент Cu"
                    ),
                ),
                (
                    "Co",
                    models.CharField(
                        blank=True, max_length=20, verbose_name="Элемент Co"
                    ),
                ),
                (
                    "Zr",
                    models.CharField(
                        blank=True, max_length=20, verbose_name="Элемент Zr"
                    ),
                ),
                (
                    "Be",
                    models.CharField(
                        blank=True, max_length=20, verbose_name="Элемент Be"
                    ),
                ),
                (
                    "Se",
                    models.CharField(
                        blank=True, max_length=20, verbose_name="Элемент Se"
                    ),
                ),
                (
                    "N",
                    models.CharField(
                        blank=True, max_length=20, verbose_name="Элемент N"
                    ),
                ),
                (
                    "Pb",
                    models.CharField(
                        blank=True, max_length=20, verbose_name="Элемент Pb"
                    ),
                ),
                (
                    "Fe",
                    models.CharField(
                        blank=True, max_length=20, verbose_name="Элемент Fe"
                    ),
                ),
                (
                    "slug",
                    models.SlugField(
                        blank=True, max_length=100, null=True, unique=True
                    ),
                ),
                ("date", models.DateTimeField(blank=True, null=True)),
                (
                    "user_search",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="metalSearch",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Metal_request",
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
                ("votes", models.IntegerField(default=0)),
                ("date", models.DateTimeField(blank=True, null=True)),
                (
                    "metals_info",
                    models.OneToOneField(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="metals_request",
                        to="metal.metal_info",
                    ),
                ),
                (
                    "user_request",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="metals_request",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="metal_info",
            name="metalsearch",
            field=models.ManyToManyField(
                blank=True, related_name="metals_info", to="metal.metalsearch"
            ),
        ),
        migrations.AddField(
            model_name="metal",
            name="metal_compound",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="metals",
                to="metal.metal_2",
            ),
        ),
    ]
