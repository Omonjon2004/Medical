from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.account_.manager import CustomUserManager
from apps.shared.models import TimeStampedModel


class Users(AbstractUser, TimeStampedModel):
    username = None
    full_name = models.CharField(max_length=255, )
    email = models.EmailField(unique=True)
    ROLE_CHOICES = (
        ('ADMIN', 'Admin'),
        ('PATIENT', 'Patient'),
        ('DOCTOR', 'Doctor'),
    )
    role = models.CharField(max_length=10,
                            choices=ROLE_CHOICES,
                            default='PATIENT'
                            )
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.full_name


class UserProfile(TimeStampedModel):
    user = models.OneToOneField(Users,
                                on_delete=models.CASCADE)
    phone_number = models.CharField(
        max_length=13,
        unique=True,
        null=True,
        blank=True)
    avatar = models.ImageField(upload_to='avatars/',
                               blank=True,
                               null=True)
