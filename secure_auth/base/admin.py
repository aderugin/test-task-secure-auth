# coding=utf-8
from django.contrib import admin
from .models import AllowedIP, AuthorizationSMS

admin.site.register(AllowedIP)
admin.site.register(AuthorizationSMS)
