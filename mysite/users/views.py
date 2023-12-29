from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeDoneView, PasswordChangeView, PasswordResetView, \
    PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, UpdateView

from users.forms import LoginUserForm, RegisterUserForm, ProfileUserForm, UserPasswordChangeForm


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
    # model = get_user_model()
    template_name = 'users/register_done.html'


class ProfileUser(LoginRequiredMixin, UpdateView):
    """ профиль пользователя """
    model = get_user_model()
    form_class = ProfileUserForm
    template_name = 'users/profile.html'
    extra_context = {'default_image': settings.DEFAULT_USER_IMAGE}

    def get_success_url(self):
        return reverse_lazy('users:profile', args=[self.request.user.pk])

    def get_object(self, queryset=None):
        return self.request.user


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
