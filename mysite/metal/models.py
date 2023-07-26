from django.contrib.auth.models import User
from django.db import models
from django.shortcuts import reverse
from transliterate import slugify
import random


class Metal_info(models.Model):
    steel = models.CharField(max_length=50, blank=True)
    steel_info = models.TextField(blank=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    metals_class = models.ForeignKey(
        'Metal_class',
        blank=True,
        null=True,
        related_name='metals_info',
        on_delete=models.CASCADE)
    metals = models.OneToOneField(
        'Metal',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    def get_absolute_url(self):
        return reverse('start_page_metal_url', kwargs={'slug': self.slug})  # TODO   post_index_url заменить

    def __str__(self):
        return self.steel

    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(f"{self.steel}__{str(random.random())[-5:-1]}")
        return super().save(*args, **kwargs)


class Metal_request(models.Model):
    votes = models.IntegerField(default=0)
    date = models.DateTimeField('date request', blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    metals_info = models.ForeignKey(
        'Metal_info',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='metals_request',
    )


class Metal_class(models.Model):
    steel_class = models.CharField(max_length=50, unique=True, blank=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    def __str__(self):
        return self.steel_class

    def get_absolute_url(self):
        return reverse('start_page_metal_url', kwargs={'slug': self.slug})  # TODO   post_index_url заменить

    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(f"{self.steel_class}_{str(random.random())[-3:-1]}")
        return super().save(*args, **kwargs)


class Metal(models.Model):
    _S = ["C", "Si", "Mn", "Cr", "Ni", "Ti", "Al", "W", "Mo", "Nb", "V", "S", "P", "Cu", "Co", "Zr", "Be", "Se", "N",
          "Pb", "Fe"]
    for i in _S:
        locals()[i] = models.CharField(max_length=20, default=0)

# def __str__(self):
#  return self.steel
