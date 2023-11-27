from django.contrib.auth.models import User
from django.db import models
from django.shortcuts import reverse

from transliterate import slugify

from metal.managers import CountManager


class Metal_info(models.Model):
    objects = models.Manager()
    count_manager = CountManager("metalsearch")

    steel = models.CharField(max_length=50, blank=True)
    steel_info = models.TextField(blank=True, verbose_name="Информация по стали")
    slug = models.SlugField(
        max_length=100, unique=True, blank=True, null=True, db_index=True
    )

    metals_class = models.ForeignKey(
        "Metal_class",
        blank=True,
        null=True,
        related_name="metals_info",
        on_delete=models.SET_NULL,
    )
    metals = models.OneToOneField(
        "Metal",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    metalsearch = models.ManyToManyField(
        "MetalSearch",
        blank=True,
        related_name="metals_info",
    )

    class Meta:
        ordering = ["steel"]
        verbose_name = "Информация по сплавам"
        verbose_name_plural = "Информация по сплавам (список)"

    def __str__(self):
        return self.steel

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(
                f"{self.steel}_{''.join(word[0] for word in self.steel_info.split())}"
            )
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("steel-slug-url", kwargs={"slug": self.slug})


class Metal_class(models.Model):
    steel_class = models.CharField(
        max_length=99, unique=True, blank=True, verbose_name="Класс стали"
    )
    slug = models.SlugField(
        max_length=100, unique=True, blank=True, null=True, db_index=True
    )

    def __str__(self):
        return self.steel_class

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.steel_class}")
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("steel-steel_class-slug-url", kwargs={"slug": self.slug})


class AbstructForMetal(models.Model):  # абстрактный класс
    _S = [
        "C",
        "Si",
        "Mn",
        "Cr",
        "Ni",
        "Ti",
        "Al",
        "W",
        "Mo",
        "Nb",
        "V",
        "S",
        "P",
        "Cu",
        "Co",
        "Zr",
        "Be",
        "Se",
        "N",
        "Pb",
        "Fe",
    ]
    for _i in _S:
        locals()[_i] = models.CharField(
            max_length=20, blank=True, verbose_name=f"Элемент {_i}"
        )

    class Meta:
        abstract = True

    @staticmethod
    def field_S(*args):  # получение полей из бд исключая определенные
        fields = [
            field for field in AbstructForMetal._meta.fields if not field.one_to_one
        ]  # явно прописываю абстрактный класс вместо self,
        # что бы можно было использовать в других
        return [fn for field in fields if (fn := field.name) not in ["id", *args]]

    def return_all(self) -> dict:  # получение ключ значение выбранных полей
        return {field: getattr(self, field) for field in self.field_S()}


class Metal(AbstructForMetal):
    metal_compound = models.OneToOneField(
        "Metal_2",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="metals",
    )

    def __str__(self):
        return str(self.id)


class Metal_2(models.Model):
    for _min, _max in [
        (f"{i}_min", f"{i}_max") for i in AbstructForMetal._S[:-1]
    ]:  # исключаем Fe
        locals()[_min] = models.FloatField(
            blank=True,
            null=True,
            db_index=True,
            verbose_name=f"Минимум элемента {_min}",
        )
        locals()[_max] = models.FloatField(
            blank=True,
            null=True,
            db_index=True,
            verbose_name=f"Максимум элемента {_max}",
        )

    def __str__(self):
        return str(self.id)

    def get_min_max(self, arg):
        min = getattr(self, f"{arg}_min")
        max = getattr(self, f"{arg}_max")
        return min, max


class MetalSearch(AbstructForMetal):
    objects = models.Manager()
    count_manager = CountManager("metals_info")
    slug = models.SlugField(
        max_length=100, unique=True, blank=True, null=True, db_index=True
    )
    date = models.DateTimeField(blank=True, null=True)
    user_search = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="metalSearch",
    )

    def __str__(self):
        return str(self.date)

    def get_absolute_url(self):
        return reverse("search-slug-url", kwargs={"slug": self.slug})


### необходимость этой модели под вопросом, так как данные в конечном итоге берутся из других таблиц ###


class Metal_request(models.Model):
    votes = models.IntegerField(default=0)
    date = models.DateTimeField(blank=True, null=True)
    metals_info = models.OneToOneField(
        "Metal_info",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="metals_request",
    )
    user_request = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="metals_request",
    )


# class SearchQuery(models.Model):
#     query = models.CharField(max_length=255, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     class Meta:
#         ordering = ['-created_at']
