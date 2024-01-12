from django.apps import apps
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.password_validation import validate_password
from django.core.validators import MinLengthValidator
from django.db import models
from django.db.models import Q


class CustomUserManager(BaseUserManager):
    """ кастомный юзер. Переопределён метод _create_user и создан метод на основе get_by_natural_key"""
    def _create_user(self, username, email, password, **extra_fields):
        """ добавлено поле secret_password. """  # todo Работа под вопросом
        if not username:
            raise ValueError("The given username must be set")
        email = self.normalize_email(email)
        GlobalUserModel = apps.get_model(
            self.model._meta.app_label, self.model._meta.object_name)
        username = GlobalUserModel.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.password = make_password(password)

        try:
            secret_password = extra_fields.get("secret_password")
            if secret_password:
                user.secret_password = make_password(secret_password)
        except Exception as e:
            print(f"Error processing secret_password: {e}")

        user.save(using=self._db)
        return user

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

    email = models.EmailField(unique=True)
    secret_login = models.CharField(max_length=128, unique=True, null=True)
    secret_email = models.EmailField(unique=True, null=True)
    secret_password = models.CharField(max_length=128, null=True,
                                       validators=[MinLengthValidator(8),
                                                   validate_password])
    user_extra_field = models.OneToOneField(
        "UserExtraField",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    REQUIRED_FIELDS = ['username']  # обязательные поля
    USERNAME_FIELD = 'email'  # вместо логина
    ALL_USERNAME_FIELD = 'email', 'username' # это кастомная константа, имеет приоритет перед USERNAME_FIELD

    def __str__(self):
        return self.first_name or self.username

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


class UserExtraField(models.Model):
    """ расширение модели юзера """
    votes = models.IntegerField(default=0)
    photo = models.ImageField(upload_to="users/%Y/%m/%d/", blank=True, null=True, verbose_name="Фотография")
    date_birth = models.DateTimeField(blank=True, null=True, verbose_name="Дата рождения")

    def __str__(self):
        return self.pk
