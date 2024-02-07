from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms

from .tools.reCaptcha import ReCaptchaField
from .tools.logic import *
from .models import *


search_fields = ["C", "Si", "Mn", "Cr", "Ni", "Ti", "Al", "W", "Mo", "Nb", "V", "S", "P", "Cu", "Co", "Zr", "Be", "Se", "N", "Pb"]


class MetalForm(forms.ModelForm):
    """Форма для получения значения % элементов,
    данные как одно число так и несколько, так же принимается "-" как указатель на исключение значения"""

    def __init__(self, *args, **kwargs):  # это для передачи начальных данных в форму
        extra_data = kwargs.pop("extra_data", None)
        super().__init__(*args, **kwargs)
        if extra_data:
            for i in extra_data:
                self.fields[i].initial = extra_data[i]

    template_name = "metal/includes/form_snippet.html"              # имя шаблона для формы, опция
    mail_checkbox = forms.BooleanField(label='Отправить почтой?', required=False)
    captcha = ReCaptchaField(label='')                      # рекапчу нужно исключить из кастомных валидаторов!

    # field_order = ['u_name'] #изменение порядка вывода форм, достаточно указать лишь определённую часть
    class Meta:
        model = MetalSearch
        fields = search_fields
        widgets = {
            field: forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Введите элемент, %"}
            )
            for field in fields
        }

    def clean(self):  # проверка для формы, а не конкретного поля
        """ Функция валидации по всем полям,
        рекапчу нужно исключить из кастомных валидаторов """
        cleaned_data = super().clean()
        captcha = self['captcha'].name
        cleaned_data.pop(captcha, None)   # captcha требует явного удаление, НЕ через генератор. И в целом ведёт себя не адекватно
        mail_checkbox = self['mail_checkbox'].name
        checkbox = cleaned_data.pop(mail_checkbox, None)  # временно удаляем, чтоб осуществить валидацию по полям
        # генерация полей с ошибками
        for field, errors in process_cleaned_data(cleaned_data):
            self.add_error(field, errors)
        # возврат значения checkbox
        if checkbox is not None and isinstance(checkbox, bool):
            cleaned_data[mail_checkbox] = checkbox
            ic(cleaned_data[mail_checkbox])

        # if self.has_error(NON_FIELD_ERRORS, code=None):
        # можно что-нибудь сделать при наличии ошибки, но для этого не нужно бросать исключение, иначе код дальше не пойдёт

    # def clean_Zr(self):
    #     field='Zr'
    #     field_data = self.cleaned_data[field]
    #     if field_data and len(field_data) > 2:
    #         self.add_error(field, ValidationError('Длина превышает 2 символа'))
    #     if self.has_error(field, code=None): # если ошибка
    #         field_data = field_data[:2]
    #     return field_data

    # def save(self, commit=True): # вызывается один раз. Метод form.save() и кверисет.save() это разные методы
    #     f = super().save(commit=False)
    #     print(f'Послупили данные в {self.Meta.model}\n')
    #     [print(f'В поле "{key}" добавлено {value}\n') for key, value in self.cleaned_data.items() if value or value==0]
    #     print('-'*25)
    #     if commit:
    #         f.save()
    #     return f

class SearchForm(forms.Form):
    """ Форма в данный момент не используется"""
    query = forms.CharField(
        validators=[],
        required=False,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Введите"}
        ),
        label="Имя пользователя",
    )  # , initial="ноунейм")

class ContactForm(forms.Form):
    """ Форма обратной связи, посылает сообщение на почту юзеру и сама себе """
    name = forms.CharField(label='Имя', max_length=255)
    email = forms.EmailField(label='Email')
    content = forms.CharField(label='', widget=CKEditorUploadingWidget())
    captcha = ReCaptchaField(label='')

class Metal_infoAdminForm(forms.ModelForm):
    """ Форма для отображения ckeditor в админ панели, для модели Metal_info """
    steel_info = forms.CharField(widget=CKEditorUploadingWidget())
    class Meta:
        model = Metal_info
        fields = '__all__'