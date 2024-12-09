from django.db import models
from apps.account_.models import Users
from apps.shared.models import TimeStampedModel
from django.core.validators import MaxValueValidator, MinValueValidator


class Doctors(TimeStampedModel):
    user_id = models.ForeignKey(Users,
                                on_delete=models.CASCADE,
                                related_name="doctors")
    specialization = models.CharField(max_length=100)
    experience_years = models.IntegerField(
        validators=[MinValueValidator(0)])
    available_times = models.TimeField()
    ratings = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)])
    bio = models.TextField()
