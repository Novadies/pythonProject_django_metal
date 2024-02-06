from smtplib import SMTPException

from django.core.mail import send_mail
from django.template.loader import render_to_string

from logs.logger import logger
from mysite.settings import DEFAULT_FROM_EMAIL

def send_results_by_email(requests, queryset):
    """ отправка письма с содержимым queryset на почту requests.user.email """
    if not requests.session.get('mail_checkbox', None):  # todo после того как будет инициализация значений нужно дополнительное тестирование
        return None
    email_subject = "Результаты поиска"
    template = "metal/email/send_results_by_email.html"   # todo заменить хост в теле письма при деплое
    email_body = render_to_string(template, {'page_obj': queryset})

    send = (
        email_subject,
        email_body,
        DEFAULT_FROM_EMAIL,
        [requests.user.email],
    )
    try:
        s = send_mail(*send, fail_silently=False, html_message=send[1])
    except SMTPException as e:
        logger.error(f'Ошибка при отправке письма. Ошибка - {e}')
    except Exception as e:
        logger.error(f'Произошло исключение: {e}')
    else:
        logger.info(f'Всего отправлено {s} писем')