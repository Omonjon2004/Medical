from django.db import models

from apps.account_.models import Users
from apps.shared.models import TimeStampedModel


# Create your models here.


class Patients(TimeStampedModel):
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    age = models.IntegerField()
    GENDER_CHOICES = [
        ('FEMALE', 'Female'),
        ('MALE', 'Male'),
    ]
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    medical_history = models.CharField(max_length=500)
    additional_phone_number = models.CharField(max_length=13)
