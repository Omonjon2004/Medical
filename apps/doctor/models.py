from django.db import models
from django.db.models import ForeignKey

from apps.account.models import Users
from apps.shared.models import TimeStampedModel


# Create your models here.


class Doctors(TimeStampedModel):
    user_id = ForeignKey(Users, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=100)
    experience_years = models.DateField()
