from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, is_staff=False, is_active=True, **extra_field):
        if not phone_number:
            raise ValueError("User must have a phone number")

        user = self.model(**extra_field)
        if password is not None:
            user.set_password(password)  # change password to hash
        user.phone_number = phone_number
        user.is_staff = is_staff
        user.is_active = is_active
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        if not password:
            raise ValueError("Superuser must have a password")
        return self.create_user(phone_number, password, is_superuser=True,
                                is_staff=True, is_active=True)


class User(AbstractUser):
    username = None
    password = models.CharField(_('password'), max_length=128, null=True, blank=True)
    phone_number = models.CharField(max_length=13, unique=True)
    chat_id = models.CharField(max_length=64, blank=True, null=True)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []
    objects = UserManager()

    def __str__(self):
        if self.last_name:
            return self.last_name
        return self.phone_number
