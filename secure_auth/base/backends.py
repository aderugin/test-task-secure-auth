# coding=utf-8
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model


class ManualModelBackend(ModelBackend):
    def authenticate(self, user=None, **kwargs):
        if user and isinstance(user, get_user_model()):
            return user
