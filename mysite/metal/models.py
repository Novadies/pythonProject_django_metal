from django.contrib.auth.models import User
from django.db import models
from django.shortcuts import reverse
from transliterate import slugify
from datetime import datetime

class Metal_info(models.Model):
    steel = models.CharField(max_length=50, blank=True, null=True)
    steel_info = models.TextField(blank=True, null=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True, null=True)
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
    metalsearch = models.ForeignKey(
        'MetalSearch',
        blank=True,
        null=True,
        related_name='metals_info',
        on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('steel-slug-url', kwargs={'slug': self.slug})

    def __str__(self):
        return self.steel

    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(f"{self.steel}_{self.id}")
        return super().save(*args, **kwargs)


class Metal_request(models.Model):
    votes = models.IntegerField(default=0)
    date = models.DateTimeField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    metals_info = models.ForeignKey(
        'Metal_info',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='metals_request',
    )


class Metal_class(models.Model):
    steel_class = models.CharField(max_length=50, unique=True, blank=True, null=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True, null=True)

    def __str__(self):
        return self.steel_class

    def get_absolute_url(self):
        return reverse('steel-steel_class-slug-url', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(f"{self.steel_class}_{self.id}") # лучше использовать id
        return super().save(*args, **kwargs)


class Metal(models.Model):
    _S = ["C", "Si", "Mn", "Cr", "Ni", "Ti", "Al", "W", "Mo", "Nb", "V", "S", "P", "Cu", "Co", "Zr", "Be", "Se", "N", "Pb", "Fe"]
    for __i in _S:
        locals()[__i] = models.CharField(max_length=20, default=0)
    @staticmethod
    def field_S(S=None):
        return [f for field in Metal._meta.fields if (f:=field.name)!=S and f != 'id']
    def return_all(self):
        return [getattr(self, field) for field in self.field_S()]
    def __str__(self):
        return str(self.id)

class MetalSearch(Metal):

    slug = models.SlugField(max_length=100, unique=True, blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)
    def save(self, *args, **kwargs):
        if not self.date:
            self.date=datetime.now()
        if not self.slug:
            spisok=["C", "Si", "Mn", "Cr", "Ni", "Ti", "Al", "W", "Mo", "Nb", "V", "S", "P", "Cu", "Co", "Zr", "Be", "Se", "N", "Pb"]
            self.slug = slugify(f"{[getattr(self,i) for i in spisok]}_{self.id}")
        return super().save(*args, **kwargs)

    def __str__(self):
        return str(self.id)
