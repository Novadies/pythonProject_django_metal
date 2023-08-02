from django import forms
from .models import *
class MetalForm(forms.ModelForm):

    class Meta:
        model = MetalSearch
        fields =["C", "Si", "Mn", "Cr", "Ni", "Ti", "Al", "W", "Mo", "Nb", "V", "S", "P", "Cu", "Co", "Zr", "Be", "Se", "N", "Pb"]
    def look(self):
        pass