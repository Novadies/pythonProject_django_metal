from django.contrib.auth import user_logged_in
from django.db.models.signals import Signal
from django.dispatch import receiver

user_logged_with_secret_password = Signal()
@receiver(user_logged_with_secret_password)
def user_logged_in_handler(sender, request, user, model, **kwargs):
    """
    Обработчик сигнала user_logged_with_secret_password, который будет вызван после успешной аутентификации пользователя,
    последством ввода секретного пароля
    """
    print(f"Пользователь {user.username} вошел в систему. Отправитель {model}")

@receiver(user_logged_in)   # стандартный сигнал при логине
def user_logged_in_handler(sender, request, user, **kwargs):
    """
    Обработчик сигнала user_logged_in, который будет вызван после успешной аутентификации пользователя.
    """
    print(f"Стандартный сигнал. Пользователь {user.username} вошел в систему")