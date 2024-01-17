from django.contrib.auth.views import LogoutView
from django.urls import path

from mysite.views import redirect_page, decorator_redirect_page
from .views import *

app_name = "users"

urlpatterns = [
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('register_done/', RegisterDone.as_view(), name='register_done'),
    path('password-change/', PasswordChange.as_view(), name='password_change'),
    path('password-change/done/', PasswordChangeDone.as_view(), name='password_change_done'),
    path('profile/', ProfileUser.as_view(), name='profile'),
    path('password-reset/',  PasswordReset.as_view(), name='password_reset'),
    path('password-reset/done/', PasswordResetDone.as_view(), name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/', PasswordResetConfirm.as_view(), name='password_reset_confirm'),
    path('password-reset/complete/', PasswordResetComplete.as_view(), name='password_reset_complete'),
    path('signup/', decorator_redirect_page('users:register')(redirect_page)),  # колхозный обход нежелательных путей из include('allauth.urls')

]
