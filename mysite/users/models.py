from django.contrib.auth.models import AbstractUser
from django.contrib.auth.password_validation import validate_password
from django.core.validators import MinLengthValidator
from django.db import models


class User(AbstractUser):
    """ дополнение базового юзера """
    secret_login = models.EmailField(unique=True, null=True)
    secret_email = models.EmailField(unique=True, null=True)
    secret_password = models.CharField(max_length=100, null=True, validators=[MinLengthValidator(8), validate_password])
    user_extra_field = models.OneToOneField(
        "UserExtraField",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    # USERNAME_FIELD = 'email'  # в теории это меняет логин на почту при входе. Нужно проверять
    def __str__(self):
        return self.first_name or self.username


class UserExtraField(models.Model):
    """ расширение модели юзера """
    votes = models.IntegerField(default=0)
    photo = models.ImageField(upload_to="users/%Y/%m/%d/", blank=True, null=True, verbose_name="Фотография")
    date_birth = models.DateTimeField(blank=True, null=True, verbose_name="Дата рождения")

    def __str__(self):
        return self.pk
