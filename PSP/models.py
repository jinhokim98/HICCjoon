from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db.models.fields import BooleanField

from .managers import CustomUserManager


class TimestampedModel(models.Model):
    objects = models.Manager()
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


class Task(models.Model):
    objects = models.Manager()
    tid = models.CharField(max_length=20, primary_key=True) #task_id
    tname = models.TextField()
    max_score = models.IntegerField()
    mid = models.ForeignKey(CustomUser, on_delete=models.CASCADE) #출제자

    def __str__(self):
        return self.Task_text


class Solution(models.Model):
    objects = models.Manager()
    sid = models.CharField(max_length=20, primary_key=True) #solution_id
    mname = models.ForeignKey(CustomUser, on_delete=models.CASCADE) #user_name
    tid = models.ForeignKey(Task, on_delete=models.CASCADE) #prob_index
    language = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    score = models.IntegerField()
    result = models.TextField()

    def __str__(self):
        return self.Solution_text