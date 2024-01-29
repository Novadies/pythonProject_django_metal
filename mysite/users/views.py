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

    def get_form_kwargs(self):
        """ Начальные значения для формы """
        kwargs = super().get_form_kwargs()
        try:
            kwargs['initial']['secret_password'] = 'Установлен' if self.get_object().secret_password else 'Отсутствует'
            kwargs['initial']['date_birth'] = self._get_user().get().user_extra_field.date_birth
            kwargs['initial']['about_user'] = self._get_user().get().user_extra_field.about_user
        except Exception as e:
            logger.warning(f'Словарь {kwargs} Произошло исключение {e}')
        return kwargs

    def form_valid(self, form):
        """ Получаем два словаря один с полями формы модели, другой связонной модели """
        model_form = {key: form.cleaned_data[key] for key in form.cleaned_data if key in self.form_class.Meta.fields}
        free_form = {key: form.cleaned_data[key] for key in form.cleaned_data if key not in model_form}

        self._get_user().update(**model_form)
        with warnings.catch_warnings():  # убрать встроенное предупреждение о часовых поясах
            warnings.simplefilter("ignore")
            self.bound_model.objects.update_or_create(to_user=self._get_user().get(),   # .get() создаёт объект
                                                      defaults=free_form)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user

    def _get_user(self):
        """ возвращает юзер в виде кверисет """
        return self.model.objects.filter(username=self.get_object().username)


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
