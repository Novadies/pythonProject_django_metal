import datetime

from ckeditor.widgets import CKEditorWidget
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm, UserChangeForm, \
    ReadOnlyPasswordHashField, UsernameField
from django import forms
from django.core.exceptions import ValidationError


class LoginUserForm(AuthenticationForm):
    """ Форма входа """
    class Meta:
        model = get_user_model()
        fields = ['username', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-input'}),
            'password': forms.PasswordInput(attrs={'class': 'form-input'})
        }
        labels = {
            'username': 'Логин',
            'password': 'Пароль'
        }
        error_messages = {
            'username': {
                'invalid': 'Логин или пароль неверны'
            },
            'password': {
                'required': 'Логин или пароль неверны.'
            }
        }
        help_texts = {
            'username': 'Не забывайте про регистр',
        }


class RegisterUserForm(UserCreationForm):
    """ Форма регистрации """
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'password1', 'password2'] # убрал поля
        labels = {
            'email': 'E-mail',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
        }
        widgets = {
            'email': forms.TextInput(attrs={'class': 'form-input'}),
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input'}),
        }

    def clean_email(self):
        field = 'email'
        email = self.cleaned_data[field]
        if self.Meta.model.objects.filter(email=email).exists():
            self.add_error(field, ValidationError("Такой E-mail уже существует!"))
        return email


class UserForm(UserChangeForm):
    """ Форма для CustomUserAdmin.
        Можно внести дополнительные поля, не связанные с моделью и соответственные методы.
    """
    pass

class ProfileUserForm(forms.ModelForm):
    """ Форма профиля пользователя"""
    this_year = datetime.date.today().year

    username = forms.CharField(disabled=True, label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.CharField(disabled=True, label='E-mail', widget=forms.TextInput(attrs={'class': 'form-input'}))
    secret_email = forms.CharField(
        label='Секретный E-mail', widget=forms.TextInput(attrs={'class': 'form-input'}), required=False)
    secret_password = forms.CharField(
        label='Секретный пароль', widget=forms.TextInput(attrs={'class': 'form-input'}), required=False, disabled=True)

    # todo нет связи с моделью UserExtraField
    date_birth = forms.DateField(widget=forms.SelectDateWidget(years=tuple(range(this_year - 100, this_year - 5))))
    about_user = forms.CharField(widget=CKEditorWidget(), required=False)
    photo = forms.ImageField(label='Выберите фото', widget=forms.FileInput(attrs={'accept': 'image/*'}), required=False)

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name', 'secret_email', 'secret_password']
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input'}),
        }


class UserPasswordChangeForm(PasswordChangeForm):
    """ Форма смены пароля """
    old_password = forms.CharField(label="Старый пароль", widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    new_password1 = forms.CharField(label="Новый пароль", widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    new_password2 = forms.CharField(label="Подтверждение пароля", widget=forms.PasswordInput(attrs={'class': 'form-input'}))
