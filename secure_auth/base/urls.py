# coding=utf-8
from django.conf.urls import url
from .views import IndexView, LoginView, LogoutView, SmsConfirmView, IPConfirmView

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^login/confirm/$', SmsConfirmView.as_view(), name='login-confirm'),
    url(r'^confirm-ip/(?P<ip>[\w-]+)/$', IPConfirmView.as_view(), name='confirm-ip')
]
