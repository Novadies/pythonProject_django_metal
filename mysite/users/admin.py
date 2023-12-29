from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from users.forms import RegisterUserForm, CustomUserChangeForm
from users.models import User


class CustomUserAdmin(UserAdmin):  # Todo не ясно для чего прописывать пользовательскую админ модель
    add_form = RegisterUserForm
    form = CustomUserChangeForm # todo а так же зачем эта форма
    model = get_user_model()
    list_display = ['email', 'username', ]


admin.site.register(User, CustomUserAdmin)
