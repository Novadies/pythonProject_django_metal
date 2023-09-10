from django import forms
from .models import *
class MetalForm(forms.ModelForm):

    class Meta:
        model = MetalSearch
        fields = [field.name for field in model._meta.fields][1:-4]
        #exclude =[]   # исключая формы
        widgets = {field: forms.TextInput(attrs={'class': 'form-control'}) for field in fields}
        # !!!!! заменить TextInput
    def look(self):
        pass