import re

from django import forms
from django.core.exceptions import ValidationError

from metal.tools.logic import If_0_value, other_value, packing
from .models import *


search_fields = ["C", "Si", "Mn", "Cr", "Ni", "Ti", "Al", "W", "Mo", "Nb", "V", "S", "P", "Cu", "Co", "Zr", "Be", "Se", "N", "Pb"]

class MetalForm(forms.ModelForm):
    def __init__(self, *args, **kwargs): # это для передачи начальных данных в форму
        extra_data = kwargs.pop('extra_data', None)
        super().__init__(*args, **kwargs)
        if extra_data:
            for i in extra_data:
                self.fields[i].initial = extra_data[i]

    template_name = "metal/includes/form_snippet.html" #имя шаблона для формы, опция
    # u_name = forms.CharField(validators=[], required=False,
    #                          widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите'}),
    #                          label="Имя пользователя")
    # field_order = ['u_name'] #изменение порядка вывода форм, достаточно указать лишь определённую часть
    class Meta:
        model = MetalSearch
        fields = search_fields
        widgets = {field: forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите элемент, %'}) for field in fields}

    def clean(self): # проверка для формы, а не конкретного поля
        cleaned_data = super().clean()
        #pattern = re.compile(r"^[-—]?\d{1,2}([.,$]\d{0,2})?$")
        pattern = re.compile(r"^([-—]?\d{1,2}([.,$]\d{0,2})?)([-—]\d{1,2}([.,$]\d{0,2})?)?$") #проверка учитывающая ввод диапазона
        zero = True
        for field in search_fields:
            f = cleaned_data.get(field)
            if f: zero = False
            else: continue
            if len(f) > 12:  self.add_error(field, ValidationError('Длина превышает 12 символа')) # ошибка будет в .error а не .non_field_errors
            if not pattern.match(f): self.add_error(field, ValidationError('Введите подходящее число'))
            else:
                try:
                    data = f.replace(',', '.').replace(' ', '').replace('—', '-')
                    cleaned_data[field] = packing(data)
                except Exception: self.add_error(field, ValidationError('Значение не проходит валидацию'))
        if zero and len(cleaned_data)==len(search_fields): raise ValidationError("Все поля пусты")
        #if self.has_error(NON_FIELD_ERRORS, code=None):
        # можно что-нибудь сделать при наличии ошибки

    # def clean_Zr(self):
    #     field='Zr'
    #     field_data= self.cleaned_data[field]
    #     if field_data:
    #         if len(field_data) > 2:
    #             raise ValidationError('Длина превышает 2 символов')
    #     #if self.has_error(field, code=None):
    #     # можно что-нибудь сделать при наличии ошибки
    #     return field_data
    @staticmethod
    def search_for_connections(cleaned_data): # ОБРАБОТКА значений из формы
        data = {key:value for key, value in cleaned_data.items() if value} # получение всех значений кроме нулевых
        only = [f'{key}_min' for key in data] + [f'{key}_max' for key in data] #получение используемых полей
        answer = Metal_2.objects.only(*only)
        answer = If_0_value(answer, cleaned_data) #обработка нулевых значений
        if data:
            for key in data:
                answer = other_value(answer, data, key)
        metal_2_to_metal = Metal.objects.filter(metal_compound__in=answer) #проход по связям
        return Metal_info.objects.filter(metals__in=metal_2_to_metal)

    # def save(self, commit=True): # вызывается один раз. Метод form.save() и кверисет.save() это разные методы
    #     f = super().save(commit=False)
    #     print(f'Послупили данные в {self.Meta.model}\n')
    #     [print(f'В поле "{key}" добавлено {value}\n') for key, value in self.cleaned_data.items() if value or value==0]
    #     print('-'*25)
    #     if commit:
    #         f.save()
    #     return f

class NotBoundsForm(forms.Form):
    u_name = forms.CharField(validators=[], required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите'}), label="Имя пользователя")#, initial="ноунейм")