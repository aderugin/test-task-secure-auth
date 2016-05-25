# coding=utf-8
from django import forms
from django.contrib.auth.forms import AuthenticationForm as BaseAuthenticationForm
from django.contrib.auth import authenticate
from .models import AllowedIP


class AuthenticationForm(BaseAuthenticationForm):
    def confirm_login_allowed(self, user):
        self.error_messages['invalid_ip'] = ('Вы сменили свое местоположение,'
                                             'письмо с подтверждением отправлено '
                                             'на Ваш email')

        if not AllowedIP.check_ip(self.request.META['REMOTE_ADDR'], user):
            AllowedIP.objects.create(
                user=user,
                ip=self.request.META['REMOTE_ADDR']
            )
            raise forms.ValidationError(
                self.error_messages['invalid_ip'],
                code='invalid_ip',
            )

        if not user.is_active:
            raise forms.ValidationError(
                self.error_messages['inactive'],
                code='inactive',
            )


class AuthSmsForm(forms.Form):
    code = forms.IntegerField(
        label='СМС код подтверждения',
        help_text='На ваш телефон был отправлен код авторизации. Kод действует 5 минут'
    )

    def __init__(self, auth_sms, *args, **kwargs):
        self.auth_sms = auth_sms
        super().__init__(*args, **kwargs)

    def clean_code(self):
        code = self.cleaned_data.get('code')
        if code != self.auth_sms.code:
            raise forms.ValidationError('Не верный код')
        return code

    def get_user(self):
        return authenticate(user=self.auth_sms.user)
