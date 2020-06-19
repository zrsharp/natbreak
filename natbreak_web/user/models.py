from django.db import models

# Create your models here.

# unit byte
DEFAULT_TRAFFIC = 1024 * 1024 * 1024 * 3


class User(models.Model):
    username = models.CharField(primary_key=True,
                                max_length=20,
                                unique=True,
                                null=False)
    nickname = models.CharField(max_length=20)
    password = models.CharField(max_length=32, null=False, default='123456')
    head_portrait = models.CharField(max_length=255)
    email = models.CharField(max_length=30, null=False)
    phone = models.CharField(max_length=16, null=False)
    signup_time = models.DateTimeField(null=False)
    network_traffic = models.BigIntegerField(default=DEFAULT_TRAFFIC)
    used_traffic = models.BigIntegerField(default=0)
