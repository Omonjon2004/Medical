from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
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
    user = models.OneToOneField(Users, on_delete=models.CASCADE)
    phone_number = models.CharField(
        max_length=13, unique=True, null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars/')


class UserCards(TimeStampedModel):
    card_name = models.CharField(max_length=50)
    card_number = models.CharField(
        max_length=16,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^\d{16}$',
                message='Card number must be exactly 16 digits.'
            )
        ]
    )
    expiration_date = models.CharField(
        max_length=5,
        validators=[
            RegexValidator(
                regex=r'^(0[1-9]|1[0-2])\/\d{2}$',
                message='Expiration date must be in MM/YY format.'
            )
        ]
    )
    cvv = models.CharField(
        max_length=3,
        validators=[
            RegexValidator(
                regex=r'^\d{3}$',
                message='CVV must be exactly 3 digits.'
            )
        ]
    )

    amount = models.FloatField()
    user_id = models.ForeignKey(to=Users,
                                on_delete=models.CASCADE, related_name='cards')


class Notifications(TimeStampedModel):
    user_id = models.ForeignKey(to=Users,
                                on_delete=models.CASCADE,
                                related_name='notifications')
    message = models.TextField()
    is_read = models.BooleanField(default=False)
