from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend, ModelBackend

from .signals import user_logged_with_secret_password


# class EmailAuthBackend(BaseBackend):
#     def authenticate(self, request, username=None, password=None, **kwargs):
#         user_model = get_user_model()
#         try:
#             user = user_model.objects.get(email=username)
#             if user.check_password(password):
#                 return user
#             return None
#         except (user_model.DoesNotExist, user_model.MultipleObjectsReturned):
#             return None
#
#     def get_user(self, user_id):
#         user_model = get_user_model()
#         try:
#             return user_model.objects.get(pk=user_id)
#         except user_model.DoesNotExist:
#             return None


class CustomAuthBackend(ModelBackend):
    """
    аутентификация из ModelBackend c измененным на user.check_secret_password(password) проверкой пароля,
    и отправкой сигнала!
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        user_model = get_user_model()
        if username is None:
            username = kwargs.get(user_model.USERNAME_FIELD)
        if username is None or password is None:
            return None
        try:
            user = user_model._default_manager.get_by_natural_key(username)
        except user_model.DoesNotExist:
            user_model().set_password(password)
        else:
            if self.user_can_authenticate(user) and user.check_secret_password(password):
                user_logged_with_secret_password.send(sender=user.__class__, request=request, user=user, model=self.__class__.__name__)
                return user
