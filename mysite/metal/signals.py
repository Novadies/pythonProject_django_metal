from smtplib import SMTPException

from django.conf import settings
from django.core.mail import send_mail, send_mass_mail, EmailMessage
from django.db.models.signals import Signal
from django.dispatch import receiver
from django.template.loader import render_to_string

from logs.logger import logger


must_send_mail_signals = Signal()

def create_turple_for_mass_mail(send: EmailMessage):
    """ аля-распаковка для send_mass_mail"""
    return send.subject, send.body, send.from_email, send.to


@receiver(must_send_mail_signals)
def send_mail_feedback(sender, form, **kwargs):
    """
    Отправка письма при заполнении формы обратной связи
    """
    name = form.cleaned_data['name']
    email = form.cleaned_data['email']
    content = form.cleaned_data['content']
    message = f'Уважаемый {name}\nВаше сообщение: "{content}"\nбудет рассмотрено в ближайшее время'

    send1 = ( # входящее письмо от юзера
        'Обратная связь',
        f'Имя: {name}\nEmail: {email}\nСообщение: {content}',
        settings.DEFAULT_FROM_EMAIL,
        [settings.DEFAULT_FROM_EMAIL],
    )
    send2 = ( # исходящее письмо юзеру
        'Благодарим за обращение',
        f'{message}',
        settings.DEFAULT_FROM_EMAIL,
        [email],
    )
    # send1.content_subtype = "html" # альтернатива html_message=send1[1]
    # send2.content_subtype = "html"
    try:
        # send_mass_mail не поддерживает html_message="html"
        s1 = send_mail(*send1, fail_silently=False, html_message=send1[1])
        s2 = send_mail(*send2, fail_silently=False, html_message=send2[1])
    except SMTPException as e:
        logger.error(f'Ошибка при отправке письма. Ошибка - {e}')
    except Exception as e:
        logger.error(f'Произошло исключение: {e}')
    else:
        logger.info(f'Всего отправлено {s1+s2} писем')

# @receiver(must_send_mail_signals)  # todo это всёравно отправляет сырой html код
def send_mass_mail_feedback(sender, form, **kwargs):
    """
    Отправка письма при заполнении формы обратной связи
    """
    name = form.cleaned_data['name']
    email = form.cleaned_data['email']
    content = form.cleaned_data['content']

    html1 = render_to_string("metal/email/send_self_email.html", {
        'name': name,
        'email': email,
        'content': content,
    })
    html2 = render_to_string("metal/email/send_feedback_email.html", {
        'name': name,
        'content': content,
    })

    send1 = ( # входящее письмо от юзера
        'Обратная связь',
        html1,
        settings.DEFAULT_FROM_EMAIL,
        [settings.DEFAULT_FROM_EMAIL],
    )
    send2 = ( # исходящее письмо юзеру
        'Благодарим за обращение',
        html2,
        settings.DEFAULT_FROM_EMAIL,
        [email],
    )
    try:
        s = send_mass_mail((send1,
                            send2),
                           fail_silently=False)
    except SMTPException as e:
        logger.error(f'Ошибка при отправке письма. Ошибка - {e}')
    except Exception as e:
        logger.error(f'Произошло исключение: {e}')
    else:
        logger.info(f'Всего отправлено {s} писем')