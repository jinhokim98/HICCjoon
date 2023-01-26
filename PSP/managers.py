from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, username, nickname, password=None, **extra_fields):
        if username is None:
            raise TypeError("Users must have a username")

        if password is None:
            raise TypeError("Users must have a password")

        if nickname is None:
            raise TypeError("Users must have a nickname")

        user = self.model(
            username=username,
            nickname=nickname,
            **extra_fields
        )

        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, password, nickname, **extra_fields):
        if username is None:
            raise TypeError("superuser must have a username")

        if password is None:
            raise TypeError("superuser must have a password")

        if nickname is None:
            raise TypeError("superuser must have a nickname")

        user = self.create_user(username, nickname, password, **extra_fields)

        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user

