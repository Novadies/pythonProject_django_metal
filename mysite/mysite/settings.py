from pathlib import Path
import os

from .custom_json_formatter import CustomJsonFormatter


BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-067oui0%zpok&cf8kzjzgb*8bsrh11i_-w2&deocx=u4j)sqnh'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []#'127.0.0.1']

INTERNAL_IPS = [
    '127.0.0.1',
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.flatpages',           # todo изменить хоста при деплое
    'django.contrib.sites',
    # инструменты отладки и мониторинга
    #'django_extensions',
    #'rest_framework'
    'simple_history',
    #'silk',
    'django_filters',
    'debug_toolbar',
    # сторонние библиотеки
    'snowpenguin.django.recaptcha3',
    'ckeditor',
    'ckeditor_uploader',  # todo попробывать загрузить изображение
    # сторонние библиотеки аутентификации
    'axes',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google', # опционально
    # приложения
    'metal',
    'users',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    #'silk.middleware.SilkyMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',


    'mysite.middleware.YourMiddlewareClass',

    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'simple_history.middleware.HistoryRequestMiddleware',

    "allauth.account.middleware.AccountMiddleware",
    'axes.middleware.AxesMiddleware',                            #  axes должен быть последним
]

ROOT_URLCONF = 'mysite.urls'
SITE_ID = 1

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],                  #  добавление папки  templates
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'mysite.context_processors.get_menu',
            ],
        },
    },
]


log_file_path = os.path.join(BASE_DIR, 'logs', 'logfile.log')
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            '()': CustomJsonFormatter,
        },
        'simple': {
            'format': '{levelname} {message} {module}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': log_file_path,
            'formatter': 'verbose',
        },
        'mail_admins': {
            'class': 'django.utils.log.AdminEmailHandler',
            'formatter': 'verbose',
        },
        'null': {
            'class': 'logging.NullHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file', 'mail_admins'],
            'level': 'INFO',
        },
        'metal': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            "propagate": False,
        },
        'debug': {
            'handlers': ['console'],
            'level': 'DEBUG',
            "propagate": False,
        },
        'django.server': {                   # исключает логи работы библиотек
            'handlers': ['null'],
            'level': 'ERROR',                # Установите уровень ERROR, чтобы отфильтровать логи этого логгера
        },
        # "django.db.backends": {            # добавление отображения SQL запросоB
        #     "handlers": ["console"],
        #     'level': 'DEBUG',
        #     "propagate": False,
        # },

    },
}

WSGI_APPLICATION = 'mysite.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
        'ATOMIC_REQUESTS': True
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 6,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


LOGIN_REDIRECT_URL = 'start-url'
LOGIN_URL = 'users:login'
LOGOUT_REDIRECT_URL = 'start-url'

AUTH_USER_MODEL = 'users.User'

AUTHENTICATION_BACKENDS = [
    'axes.backends.AxesStandaloneBackend',                     #  axes должен быть первым
    'allauth.account.auth_backends.AuthenticationBackend',
    # 'django.contrib.auth.backends.ModelBackend',
    'users.authentication.EmailOrLoginBackend',
    'users.authentication.CustomAuthBackend',
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
#STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_ROOT = BASE_DIR / 'media'
MEDIA_URL = '/media/'
DEFAULT_USER_IMAGE = MEDIA_URL + 'users/default.png'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


""" джанго AXES """
AXES_USERNAME_FORM_FIELD = 'login' # переопределяем поле для django-allauth
AXES_ENABLED = False#True                # выключить axes
AXES_FAILURE_LIMIT = 3
AXES_LOCK_OUT_AT_FAILURE = True    # блокировать или нет
AXES_COOLOFF_TIME = 1              # часа
AXES_RESET_ON_SUCCESS = True
# AXES_WHITELIST_CALLABLE = 'users.whitelist' # белый лист, функция не определена!
AXES_NEVER_LOCKOUT_WHITELIST = True

""" джанго allauth """
# ACCOUNT_EMAIL_REQUIRED = True
# ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_USERNAME_BLACKLIST = ["admin", "administrator", "moderator"]
ACCOUNT_MAX_EMAIL_ADDRESSES = 3
ACCOUNT_LOGIN_ATTEMPTS_LIMIT = None # количество неудачных попыток входа в систему

SOCIALACCOUNT_PROVIDERS = {    # todo при регистрации указывался localhost
    'google': {
        'APP': {
            'client_id': '191735540274-vp3kiqb88djb2ubuepu5tm59jeied4ql.apps.googleusercontent.com',
            'secret': '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',
            'key': ''
        },
        # 'EMAIL_AUTHENTICATION': True,
        }
    }

""" reCAPTCHA """
RECAPTCHA_PUBLIC_KEY = '6Levk0spAAAAABWWfA2tHLHqguqDlFBq6KAWc8G6'
RECAPTCHA_PRIVATE_KEY = '6Levk0spAAAAAOKDpQ2-vBo9yOJ7Pt4W51gaK8Cu'
RECAPTCHA_DEFAULT_ACTION = 'generic'
RECAPTCHA_SCORE_THRESHOLD = 0.5

""" настройки безопасности"""
SESSION_COOKIE_SECURE = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
CSP_DEFAULT_SRC = ("'self'",)

""" кэширование """
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': os.path.join(BASE_DIR, 'my_cache'),
        'TIMEOUT': 60,
    }
}

""" настройки почтового сервера """
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.yandex.ru"
EMAIL_PORT = 465
EMAIL_HOST_USER = "alekseirysyuk@yandex.ru"
EMAIL_HOST_PASSWORD = "pbjbyoscbxgivqhh"
EMAIL_USE_SSL = True
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
SERVER_EMAIL = EMAIL_HOST_USER
EMAIL_ADMIN = EMAIL_HOST_USER


""" CKEDITOR """
CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_CONFIGS = {
    'default': {
        'skin': 'moono',
        # 'skin': 'office2013',
        'toolbar_Basic': [
            ['Source', '-', 'Bold', 'Italic']
        ],
        'toolbar_YourCustomToolbarConfig': [
            {'name': 'document', 'items': ['Source', '-', 'Save', 'NewPage', 'Preview', 'Print', '-', 'Templates']},
            {'name': 'clipboard', 'items': ['Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord', '-', 'Undo', 'Redo']},
            {'name': 'editing', 'items': ['Find', 'Replace', '-', 'SelectAll']},
            {'name': 'forms',
             'items': ['Form', 'Checkbox', 'Radio', 'TextField', 'Textarea', 'Select', 'Button', 'ImageButton',
                       'HiddenField']},
            '/',
            {'name': 'basicstyles',
             'items': ['Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript', '-', 'RemoveFormat']},
            {'name': 'paragraph',
             'items': ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Blockquote', 'CreateDiv', '-',
                       'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock', '-', 'BidiLtr', 'BidiRtl',
                       'Language']},
            {'name': 'links', 'items': ['Link', 'Unlink', 'Anchor']},
            {'name': 'insert',
             'items': ['Image', 'Flash', 'Table', 'HorizontalRule', 'Smiley', 'SpecialChar', 'PageBreak', 'Iframe']},
            '/',
            {'name': 'styles', 'items': ['Styles', 'Format', 'Font', 'FontSize']},
            {'name': 'colors', 'items': ['TextColor', 'BGColor']},
            {'name': 'tools', 'items': ['Maximize', 'ShowBlocks']},
            {'name': 'about', 'items': ['About']},
            '/',  # put this to force next toolbar on new line
            {'name': 'yourcustomtools', 'items': [
                # put the name of your editor.ui.addButton here
                'Preview',
                'Maximize',

            ]},
        ],
        'toolbar': 'YourCustomToolbarConfig',  # put selected toolbar config here
        # 'toolbarGroups': [{ 'name': 'document', 'groups': [ 'mode', 'document', 'doctools' ] }],
        # 'height': 291,
        # 'width': '100%',
        # 'filebrowserWindowHeight': 725,
        # 'filebrowserWindowWidth': 940,
        # 'toolbarCanCollapse': True,
        # 'mathJaxLib': '//cdn.mathjax.org/mathjax/2.2-latest/MathJax.js?config=TeX-AMS_HTML',
        'tabSpaces': 4,
        'extraPlugins': ','.join([
            'uploadimage', # the upload image feature
            # your extra plugins here
            'div',
            'autolink',
            'autoembed',
            'embedsemantic',
            'autogrow',
            # 'devtools',
            'widget',
            'lineutils',
            'clipboard',
            'dialog',
            'dialogui',
            'elementspath'
        ]),
    }
}