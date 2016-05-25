# coding=utf-8
from datetime import datetime
from django.views.generic import View, TemplateView
from django.http import HttpResponseRedirect, Http404
from django.utils.decorators import method_decorator
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.urlresolvers import reverse, reverse_lazy

from .forms import AuthenticationForm, AuthSmsForm
from .models import AuthorizationSMS, AllowedIP


class IndexView(TemplateView):
    template_name = 'index.html'

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class LoginView(TemplateView):
    template_name = 'login.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return HttpResponseRedirect(request.GET.get('next', '/'))
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            self.create_auth_sms(form.get_user())
            return HttpResponseRedirect(reverse('login-confirm'))
        return self.render_to_response(
            self.get_context_data(form=form)
        )

    def create_auth_sms(self, user):
        auth_sms = AuthorizationSMS.objects.create(user=user)
        self.request.session['auth_sms_id'] = auth_sms.id

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = kwargs.get('form', AuthenticationForm())
        return context


class SmsConfirmView(TemplateView):
    template_name = 'login.html'

    def dispatch(self, request, *args, **kwargs):
        auth_sms = self.get_auth_sms()
        if auth_sms:
            self.auth_sms = auth_sms
            return super().dispatch(request, *args, **kwargs)
        return HttpResponseRedirect(reverse('login'))

    def get_auth_sms(self):
        auth_sms = None
        if 'auth_sms_id' in self.request.session:
            try:
                auth_sms = AuthorizationSMS.objects.get(
                    id=self.request.session['auth_sms_id'],
                    expire__gt=datetime.now()
                )
            except AuthorizationSMS.DoesNotExist:
                del self.request.session['auth_sms_id']
        return auth_sms

    def post(self, request, *args, **kwargs):
        form = AuthSmsForm(self.auth_sms, request.POST)
        if form.is_valid():
            login(request, form.get_user())
            self.auth_sms.delete()
            del self.request.session['auth_sms_id']
            return HttpResponseRedirect(reverse('index'))
        return self.render_to_response(
            self.get_context_data(form=form)
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = kwargs.get('form', AuthSmsForm(self.auth_sms))
        return context


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            logout(request)
        return HttpResponseRedirect(request.GET.get('next', '/'))


class IPConfirmView(View):
    def get(self, request, *args, **kwargs):
        try:
            allowed_ip = AllowedIP.objects.get(confirm_code=kwargs['ip'])
        except AllowedIP.DoesNotExist:
            raise Http404
        allowed_ip.confirmed = True
        allowed_ip.save()
        messages.success(request, 'Ваша новая локация подтверждена')
        return HttpResponseRedirect(reverse('login'))
