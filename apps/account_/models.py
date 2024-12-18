from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.account_.manager import CustomUserManager
from apps.shared.models import TimeStampedModel
from phonenumber_field.modelfields import PhoneNumberField

class Users(AbstractUser, TimeStampedModel):
    username = None
    full_name = models.CharField(max_length=255, )
    email = models.EmailField(unique=True)
    ROLE_CHOICES = (
        ('PATIENT', 'Patient'),
        ('ADMIN', 'Admin'),
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
    user = models.OneToOneField(
        Users,
        on_delete=models.CASCADE,
        related_name="profile"
    )
    phone_number = PhoneNumberField(
        unique=True,
        null=True,
        blank=True,
        verbose_name="Phone Number",
        region="UZ"  # Telefon raqamni O‘zbekiston bo‘yicha validatsiya qiladi
    )
    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True,
        verbose_name="Avatar"
    )

    def __str__(self):
        return f"{self.user.full_name}'s Profile"
