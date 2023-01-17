from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db.models.fields import BooleanField

from .managers import CustomUserManager


class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-created_at', '-updated_at']


class CustomUser(AbstractUser, PermissionsMixin, TimestampedModel):
    nickname = models.CharField(max_length=5)
    is_active = BooleanField(default=True)
    is_staff = BooleanField(default=False)

    REQUIRED_FIELDS = ['nickname']

    objects = CustomUserManager()

    def get_full_name(self):
        return self.nickname


