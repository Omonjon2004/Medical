from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

from apps.shared.models import TimeStampedModel


class Users(AbstractUser, TimeStampedModel):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=13, unique=True)
    ROLE_CHOICES = (
        ('ADMIN', 'Admin'),
        ('PATIENT', 'Patient'),
        ('DOCTOR', 'Doctor'),
    )
    role = models.CharField(max_length=10,
                            choices=ROLE_CHOICES,
                            default='PATIENT')

    avatar = models.ImageField(upload_to='avatars/')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.get_full_name()


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
