# coding=utf-8
import uuid
from random import randint
from datetime import datetime, timedelta

from django.db import models
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.dispatch import receiver
from django.core.urlresolvers import reverse


def _get_expire():
    return datetime.now() + timedelta(minutes=5)


def _get_random_code():
    return randint(11111, 99999)


def _get_confirm_code():
    return str(uuid.uuid1())


class AllowedIP(models.Model):
    confirmed = models.BooleanField(default=False)
    user = models.ForeignKey(User, related_name='allowed_ips')
    ip = models.CharField(max_length=15)
    confirm_code = models.CharField(max_length=100, default=_get_confirm_code)

    @classmethod
    def check_ip(cls, ip, user):
        return cls.objects.filter(ip=ip, user=user, confirmed=True).exists()

    def get_confirm_url(self):
        return 'http://{0}{1}'.format(
            Site.objects.get_current(),
            reverse('confirm-ip', args=(self.confirm_code,))
        )


@receiver(models.signals.post_save, sender=AllowedIP)
def allowed_ip_save_handler(sender, instance, created, **kwargs):
    if created:
        # Some Email backend
        print('===========================EMAIL===============================')
        print(instance.ip, instance.get_confirm_url())
        print('===============================================================')


class AuthorizationSMS(models.Model):
    user = models.ForeignKey(User)
    code = models.PositiveIntegerField(default=_get_random_code)
    expire = models.DateTimeField(default=_get_expire)

    @classmethod
    def cleanup(cls):
        cls.objects.filter(expire__lt=datetime.now()).delete()


@receiver(models.signals.post_save, sender=AuthorizationSMS)
def auth_sms_save_handler(sender, instance, created, **kwargs):
    if created:
        # Some SMS backend
        print('=============================SMS===============================')
        print(instance.user.username, instance.code)
        print('===============================================================')
