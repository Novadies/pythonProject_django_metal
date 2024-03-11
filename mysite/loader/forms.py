from django import forms
from django.core.validators import FileExtensionValidator, MaxLengthValidator

from loader.models import UploadFiles


class UploadFileForm(forms.ModelForm):
    """ базовый класс в котором определяется форма для загрузки"""
    file_to_upload = forms.FileField(label='', required=True,
                                     widget=forms.FileInput(attrs={'accept': '.xlsx,.xlsm',
                                                                   # .csv', # todo  csv пока не читаем
                                                                   'id': 'exel_files'}),
                                     validators=[  # MaxLengthValidator(max_size=5242880),
                                         # FileExtensionValidator(allowed_extensions= ['xlsx', 'xlsm', 'csv']),
                                     ],
                                     )

    class Meta:
        model = UploadFiles
        fields = ['file_to_upload']
