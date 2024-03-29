from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth.models import Group

from users.forms import RegisterUserForm, UserForm
from users.models import User, UserExtraField

admin.site.unregister(Group)
@admin.register(Group)
class CustomGroupAdmin(GroupAdmin):
    """ запрет на создание и тд. групп (в частости Группы), в том числе с правами пользователя """
    def has_add_permission(self, request):
        return request.user.is_superuser
    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

class ExtraUserInline(admin.StackedInline):
    model = UserExtraField
    verbose_name = 'Дополнительные поля пользователя'
    fieldsets = (
            ('Дополнительная информация', {'fields': ('votes', 'photo')}),
            ('О пользователе', {'fields': ('date_birth', 'about_user',)}),
        )
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    form = UserForm
    add_form = RegisterUserForm     # здесь нужно просто указать свою форму регистрации наследуемую от UserCreationForm
    model = get_user_model()
    list_display = ['email', 'username', "is_staff"]    # отображение в корневой папке Пользователи
    readonly_fields = ['secret_password']
    inlines = (ExtraUserInline,)
    fieldsets = (
        ('Основные данные', {'fields': ('username', 'password', 'email')}),
        ('ФИО', {'fields': ('first_name', 'last_name',), 'classes': ('collapse',)}),
        ('Права', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Важные даты', {'fields': ('last_login', 'date_joined')}),
        ('Дополнительная аутентификация', {'fields': ('secret_email', 'secret_password',)}),
    )

    def get_readonly_fields(self, request, obj=None):
        """ Запретить пользователям, не являющимся суперпользователями,
        редактировать свои и чужие разрешения и группы разрешений,
        а так же дополнительные выбранные поля"""
        extra_all_disabled_fields = ()                  # запрет на редактирование для Не суперпользователей
        extra_self_disabled_fields  = ('username',)     # запрет на редактирование своих полей
        extra_staff_disabled_fields = ('groups',)                # запрет на редактирование других staff
        readonly_fields = set(self.readonly_fields)
        if not request.user.is_superuser:               # запрет на изменение прав и полей
            readonly_fields |= {
                'is_superuser',
                'user_permissions',
                'is_staff',
                *extra_all_disabled_fields,
            }
            if obj is not None:
                if obj == request.user:             # запрет на редактирование СОБСТВЕННЫХ полей
                    readonly_fields |= {
                        'groups',
                        *extra_self_disabled_fields,
                    }
                if obj.is_superuser:                # запрет на редактирование superuser
                    readonly_fields |= {
                        'is_active',
                        'username',
                        'email',
                        'groups',
                    }
                if obj.is_staff:                    # запрет на редактирование staff
                    readonly_fields |= {
                        'username',
                        'email',
                        *extra_staff_disabled_fields,
                    }
        return readonly_fields

    """ общие разрешения для работы с моделями """
    def has_add_permission(self, request):
        return request.user.is_superuser
    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.is_staff
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def get_actions(self, request):
        """ Скрываем actions для пользователей без определённых разрешений"""
        actions = super().get_actions(request)
        perm = 'auth.view_user', 'auth.change_user'  # необходимые разрешения или @admin.action(permissions=["change"])
        actions_disabled =[]                                       # запрещённые action
        if not request.user.has_perm(*perm):
            actions = {k: v for k, v in actions.items() if k not in actions_disabled}
        return actions

    def get_form(self, request, obj=None, **kwargs):
        # if request.user.is_superuser:
        #     kwargs["form"] = MySuperuserForm
        return super().get_form(request, obj, **kwargs)

    def lookup_allowed(self, lookup, value):
        """ Запретить поиск паролей """
        return not lookup.startswith("secret_password") and super().lookup_allowed(lookup, value)


