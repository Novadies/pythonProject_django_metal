from django import forms
from .models import *
class MetalForm(forms.ModelForm):

    file=forms.FileField()
    class Meta:
        model = Metal_info
        fields =["steel", "steel_info", "slug"]
    def look(self):
        pass