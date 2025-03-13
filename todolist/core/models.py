from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    '''
    Modifying create_superuser to assign custom field role=ADMIN to superuser
    '''

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('role', RoleChoices.ADMIN)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        return self.create_user(email, password, **extra_fields)


class RoleChoices(models.IntegerChoices):
    USER = 1, 'user'
    ADMIN = 2, 'admin'


class CustomUser(AbstractUser):
    role = models.IntegerField(choices=RoleChoices, default=RoleChoices.USER)
    is_banned = models.BooleanField(default=False)

    objects = CustomUserManager()

    def has_perm(self, perm, obj=None):
        return self.role == RoleChoices.ADMIN

    def has_module_perms(self, app_label):
        return self.role == RoleChoices.ADMIN

    def __str__(self):
        return self.email
