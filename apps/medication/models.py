from django.db import models

from apps.shared.models import TimeStampedModel


# Create your models here.


class Medications(TimeStampedModel):
    name = models.CharField(max_length=255)
    description = models.TextField()
    DOSAGE_FORM_CHOICES = (
        ('SYRUP', 'Syrup'),
        ('CREAM', 'Cream'),
        ('TABLET', 'Tablet'),
        ('CAPSULE', 'Capsule')
    )
    dosage_form = models.CharField(choices=DOSAGE_FORM_CHOICES, max_length=20)
    strength = models.CharField(max_length=20)
    price = models.FloatField()
    stock_quantity = models.IntegerField()
    manufacturer = models.CharField(max_length=255)
