import re

from django import forms
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS


from .models import *

search_fields = ["C", "Si", "Mn", "Cr", "Ni", "Ti", "Al", "W", "Mo", "Nb", "V", "S", "P", "Cu", "Co", "Zr", "Be", "Se", "N", "Pb"]

class MetalForm(forms.ModelForm):
    template_name = "metal/includes/form_snippet.html" #имя шаблона для формы, опция
    # u_name = forms.CharField(validators=[], required=False,
    #                          widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите'}),
    #                          label="Имя пользователя")
    # field_order = ['u_name'] #изменение порядка вывода форм, достаточно указать лишь определённую часть
    class Meta:
        model = MetalSearch
        fields = search_fields
        widgets = {field: forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите элемент'}) for field in fields}

    def clean(self): # проверка для формы, а не конкретного поля
        cleaned_data = super().clean()
        pattern = re.compile(r"^\d{1,2}([.,$]\d{0,2})?$")
        zero = True
        for field in search_fields:
            f = cleaned_data.get(field)
            if f: zero = False
            else: continue
            if len(f) > 5:  self.add_error(field, ValidationError('Длина превышает 5 символа')) # ошибка будет в .error а не .non_field_errors
            elif not pattern.match(f): self.add_error(field, ValidationError('Введите десятичное число'))
            else: cleaned_data[field] = float(f.replace(',', '.').replace(' ', ''))
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
    def search_for_connections(cleaned_data):
        data = {key:value for key, value in cleaned_data.items() if value}
        data_0 = [key for key, value in cleaned_data.items() if value==0]
        data_min_0 = [f'{key}_min' for key in data_0]  # вычисления для .values .По идее оптимизирует, так как поля по которым нет фильтрации не загружаются
        #answer = Metal_2.objects.values('id', *data_min_0, *[f'{key}_min' for key in list(data)], *[f'{key}_max' for key in list(data)])
        answer = Metal_2.objects.all()
        if data_0:
            for key in data_min_0:
                key_model = {key: float(0)}
                answer = answer.filter(**key_model)
        if data:
            for key in data:
                key_model_lte = {f'{key}_min__lte': data[key]}
                key_model_gte = {f'{key}_max__gte': data[key]}
                answer = answer.filter(**key_model_lte, **key_model_gte)
        print(answer.count())
        metal_2_to_metal = Metal.objects.filter(metal_compound__in=answer)
        return Metal_info.objects.filter(metals__in=metal_2_to_metal)

    def save(self, commit=True): # вызывается один раз. Метод form.save() и кверисет.save() это разные методы
        f = super().save(commit=False)
        print(f'Послупили данные в {self.Meta.model}\n')
        [print(f'В поле "{key}" добавлено {value}\n') for key, value in self.cleaned_data.items() if value or value==0]
        print('-'*25)
        if commit:
            f.save()
        return f

class NotBoundsForm(forms.Form):
    u_name = forms.CharField(validators=[], required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите'}), label="Имя пользователя")#, initial="ноунейм")