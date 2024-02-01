from django.contrib.auth import user_logged_in, user_login_failed
from django.db.models.signals import Signal
from django.dispatch import receiver

from logs.logger import logger

user_logged_with_secret_password = Signal()
change_view = Signal()
@receiver(user_logged_with_secret_password)
def user_logged_in_handler(sender, request, user, model, **kwargs):  # не забывать экспортировать в apps
    """
    Обработчик сигнала user_logged_with_secret_password, который будет вызван после успешной аутентификации пользователя,
    последством ввода секретного пароля
    """
    logger.info(f"Пользователь {user.username} вошел в систему с помощью секретного пароля. Бэкенд {model}. Отправитель")

@receiver(user_logged_in)   # стандартный сигнал при логине
def user_logged_in_handler(sender, request, user, **kwargs):
    """
    Обработчик сигнала user_logged_in, который будет вызван ВСЕГДА после успешной аутентификации пользователя
    ЛЮБЫМ бэкендом.
    """
    logger.info(f"Стандартный сигнал. Пользователь {user.username} вошел в систему. Отправитель ")
        
@receiver(user_login_failed)  # стандартный сигнал при неудачном входе
def handle_login_failed(sender, credentials, request, **kwargs):
    """ здесь можно что-то сделать с неудачными попытками входа """
    logger.info(f"Попытка неудачного входа: {credentials}")
