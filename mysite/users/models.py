from ckeditor_uploader.fields import RichTextUploadingField
from django.apps import apps
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.models import AbstractUser, UserManager
from django.contrib.auth.password_validation import validate_password
from django.core.validators import MinLengthValidator
from django.db import models
from django.db.models import Q


class CustomUserManager(UserManager):
    """ кастомный юзер. Cоздан метод на основе get_by_natural_key"""

    def get_by_natural_key_v2(self, username):
        """ используется кастомный ALL_USERNAME_FIELD """
        all_fields = getattr(self.model, "ALL_USERNAME_FIELD", None)
        if all_fields is not None:
            conditions = Q()
            for field in all_fields:
                conditions |= Q(**{field: username})
            return self.get(conditions)
        else:
            return self.get_by_natural_key(username)


class User(AbstractUser):
    """ дополнение базового юзера """
    objects = CustomUserManager()

    email = models.EmailField(unique=True, null=True)
    secret_email = models.EmailField(unique=True, null=True, default=None)
    secret_password = models.CharField(max_length=128, null=True, default=None,
                                       validators=[MinLengthValidator(8),
                                                   validate_password])

    REQUIRED_FIELDS = ['username']  # обязательные поля
    USERNAME_FIELD = 'email'  # вместо логина
    ALL_USERNAME_FIELD = 'email', 'username' # это кастомная константа, имеет приоритет перед USERNAME_FIELD

    def __str__(self):
        return self.first_name or self.username

    def save(self, *args, **kwargs):
        """ Иначе email будут пустыми, что выкинет ошибку """
        fields_to_check = ['email', 'secret_email', 'secret_password']
        for field in fields_to_check:
            if getattr(self, field) == "":
                setattr(self, field, None)
        super().save(*args, **kwargs)

    def check_secret_password(self, raw_password):
        """ зеркальный обычному check_password но для secret_password"""
        def setter(raw_password):
            self.set_secret_password(raw_password)
            self._password = None
            self.save(update_fields=["secret_password"])
        #setter(raw_password) # Attention! это устанавливает новый пароль и хэширует его в бд
        return check_password(raw_password, self.secret_password, setter)

    def set_secret_password(self, raw_password):
        self.secret_password = make_password(raw_password)
        self._password = raw_password


class UserExtraField(models.Model): # todo есть ли возможность работать в связки с основной моделью?
    """ расширение модели юзера """
    votes = models.IntegerField(default=0)
    photo = models.ImageField(upload_to="users/%Y/%m/%d/", blank=True, null=True, verbose_name="Фотография")
    date_birth = models.DateTimeField(blank=True, null=True, verbose_name="Дата рождения")
    about_user = RichTextUploadingField(blank=True)

    user_extra_field = models.OneToOneField(
        "User",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    def __str__(self):
        return f'{self.pk}'
