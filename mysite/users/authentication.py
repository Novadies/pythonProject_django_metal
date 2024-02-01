from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

from .signals import user_logged_with_secret_password

def authenticate(request, username=None, password=None, **kwargs):
    """ часть функции ModelBackend.authenticate с дополненным user-ом """
    user_model = get_user_model()
    username = username or kwargs.get(user_model.USERNAME_FIELD)
    if username is None or password is None:
        return None
    try:
        user = user_model._default_manager.get_by_natural_key_v2(username)
    except user_model.DoesNotExist:
        user_model().set_password(password)
    else:
        return user

class EmailOrLoginBackend(ModelBackend):
    """ стандартная аутентификация за исключением , что на вход как логин так и email """
    def authenticate(self, request, username=None, password=None, **kwargs):
        user = authenticate(request, username, password, **kwargs)
        if user is not None and user.check_password(password):
            return user if self.user_can_authenticate(user) else None


class CustomAuthBackend(ModelBackend):
    """
    аутентификация из ModelBackend c измененным на user.check_secret_password(password) проверкой пароля,
    и отправкой сигнала!
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        user = authenticate(request, username, password, **kwargs)
        if user is not None and self.user_can_authenticate(user) and user.check_secret_password(password):
            user_logged_with_secret_password.send(
                sender=user.__class__, request=request, user=user, model=self.__class__.__name__)
            request.session['invisible_mod'] = 'true'           # добавляем в сессию информацию
            return user
