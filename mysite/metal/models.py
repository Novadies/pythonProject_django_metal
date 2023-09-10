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

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.steel}_{''.join(word[0] for word in self.steel_info.split())}")
        return super().save(*args, **kwargs)

    class Meta:
        ordering = ['steel']

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

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.steel_class}")
        return super().save(*args, **kwargs)


class Metal(models.Model):
    _S = ["C", "Si", "Mn", "Cr", "Ni", "Ti", "Al", "W", "Mo", "Nb", "V", "S", "P", "Cu", "Co", "Zr", "Be", "Se", "N", "Pb", "Fe"]
    for __i in _S:
        locals()[__i] = models.CharField(max_length=20, default=0)
    metal_compound = models.OneToOneField(
        'Metal_2',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    @staticmethod
    def field_S(*args):
        fields = [field for field in Metal._meta.fields if not field.one_to_one]
        return [fn for field in fields if (fn := field.name) not in ['id', *args]]


    def return_all(self):
        return {field : getattr(self, field) for field in self.field_S()}
    def __str__(self):
        return str(self.id)

class Metal_2(models.Model):
    for __min, __max in [(f'{i}_min', f'{i}_max') for i in Metal._S[:-1]]:
        locals()[__min] = models.FloatField(blank=True, null=True, db_index=True)
        locals()[__max] = models.FloatField(blank=True, null=True, db_index=True)
    def get_min_max(self, arg):
        min = getattr(self, f'{arg}_min')
        max = getattr(self, f'{arg}_max')
        return min, max
    def __str__(self):
        return str(self.id)

class MetalSearch(Metal):

    slug = models.SlugField(max_length=100, unique=True, blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)
    def save(self, *args, **kwargs):
        if not self.date:
            self.date=datetime.now()
        if not self.slug:
            self.slug = slugify(f"{'_'.join(map(str, [getattr(self,i) for i in self.field_S('Fe')]))}_{self.id}")
        return super().save(*args, **kwargs)

    def __str__(self):
        return str(self.id)
