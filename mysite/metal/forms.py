from django import forms

class MetalForm(forms.ModelForm):
    title=forms.CharField(max_length=50)
    slug=forms.CharField(max_length=50)
    
    def look(self):
        pass