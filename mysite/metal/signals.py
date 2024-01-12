from smtplib import SMTPException

from django.core.mail import send_mail, send_mass_mail
from django.db.models.signals import Signal
from django.dispatch import receiver

from logs.logger import logger
from mysite.settings import DEFAULT_FROM_EMAIL

must_send_mail_signals = Signal()
@receiver(must_send_mail_signals)
def send_mail_feedback(sender, form, **kwargs):
    """
    Отправка письма при заполнении формы обратной связи
    """
    name = form.cleaned_data['name']
    email = form.cleaned_data['email']
    content = form.cleaned_data['content']
    message = f'Уважаемый {name}\nВаше сообщение: "{content}"\nбудет рассмотрено в ближайшее время'
    print(email, DEFAULT_FROM_EMAIL)
    send1 = ( # входящее письмо от юзера
        'Обратная связь',
        f'Имя: {name}\nEmail: {email}\nСообщение: {content}',
        DEFAULT_FROM_EMAIL,
        [DEFAULT_FROM_EMAIL],
    )
    send2 = ( # исходящее письмо юзеру
        'Благодарим за обращение',
        f'{message}',
        DEFAULT_FROM_EMAIL,
        [email],
    )
    try:
        s = send_mass_mail((send1 , send2), fail_silently=False)
    except  SMTPException as e:
        logger.error(f'Ошибка при отправке письма. Ошибка - {e}')
    except Exception as e:
        logger.error(f'Произошло исключение: {e}')
    else:
        logger.info(f'Всего отправлено {s} писем')
