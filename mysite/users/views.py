import warnings

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeDoneView, PasswordChangeView, PasswordResetView, \
    PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, UpdateView

from logs.logger import logger
from .forms import LoginUserForm, RegisterUserForm, ProfileUserForm, UserPasswordChangeForm, \
    UserPasswordSecretChangeForm
from .models import UserExtraField


class LoginUser(LoginView):
    """ вход в учётную запись """
    form_class = LoginUserForm
    template_name = 'users/login.html'

    # def get_success_url(self):
    #     """ перенаправление, самый высокий приоритет """
    #     return reverse_lazy('start-url')


class RegisterUser(CreateView):
    """ регистраци я пользователя """
    form_class = RegisterUserForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:register_done')


class RegisterDone(TemplateView):
    """ пользователь успешно зарегистрирован """
    template_name = 'users/register_done.html'


class ProfileUser(LoginRequiredMixin, UpdateView):
    """ профиль пользователя """
    form_class = ProfileUserForm
    model = form_class.Meta.model
    bound_model = UserExtraField
    template_name = 'users/profile.html'
    extra_context = {'default_image': settings.DEFAULT_USER_IMAGE}

    def get_initial(self):
        """ Начальные значения для формы """
        initial = super().get_initial()
        # статус secret_password не должен показываться как 'Установлен' если аутентификация произошла посредством него же
        initial['secret_password'] = 'Отсутствует' \
            if (self.request.session.get('invisible_mod') == 'true' or not self.object.secret_password) \
            else 'Установлен'
        initial['date_birth'] = self.object.user_extra_field.date_birth
        initial['about_user'] = self.object.user_extra_field.about_user
        return initial

    def form_valid(self, form):
        """ Получаем два словаря один с полями формы модели, другой связонной модели """
        model_form = {key: form.cleaned_data[key] for key in form.cleaned_data if key in self.form_class.Meta.fields}
        free_form = {key: form.cleaned_data[key] for key in form.cleaned_data if key not in model_form}
        """ использование update налагает много ограничений, есть ли в нём смысл? """
        self.model.objects.filter(pk=self.object.pk).update(**model_form)  # обновление model (юзера)
        with warnings.catch_warnings():   # убрать бессмысленный RuntimeWarning
            warnings.simplefilter("ignore")
            self.bound_model.objects.update_or_create(to_user=self.object,   # обновление связанной модели
                                                      defaults=free_form)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        """ явный поиск пользователя, лучше использовать pk.
            А так же select_related.
            Возвращает self.object
        """
        return self.model.objects.select_related('user_extra_field').filter(pk=self.request.user.pk).first()

class PasswordChange(PasswordChangeView):
    """ изменение пароля """
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy("users:password_change_done")
    template_name = "users/password_actions/password_change_form.html"


class PasswordChangeDone(PasswordChangeDoneView):
    """ успешное изменение пароля """
    template_name = "users/password_actions/password_change_done.html"


class PasswordReset(PasswordResetView):
    """ запрос на сброс пороля """
    template_name = "users/password_actions/password_reset_form.html"
    email_template_name = "users/password_actions/password_reset_email.html"
    success_url = reverse_lazy("users:password_reset_done")


class PasswordResetDone(PasswordResetDoneView):
    """ письмо на сброс отправлено"""
    template_name = "users/password_actions/password_reset_done.html"


class PasswordResetConfirm(PasswordResetConfirmView):
    """ ввод нового пароля """
    template_name = "users/password_actions/password_reset_confirm.html"
    success_url = reverse_lazy("users:password_reset_complete")


class PasswordResetComplete(PasswordResetCompleteView):
    """ пароль успешно восстановлен """
    template_name = "users/password_actions/password_reset_complete.html"


class PasswordeSecretChange(PasswordChangeView):
    """ изменение секретного пароля """
    form_class = UserPasswordSecretChangeForm
    success_url = reverse_lazy("users:password_change_done")
    template_name = "users/password_actions/password_change_secret_form.html"

    def form_valid(self, form):
        """ Переопределение, чтоб убрать выход из сеансов,
        здесь это поведение бессмысленно.
        """
        return super().form_valid(form)