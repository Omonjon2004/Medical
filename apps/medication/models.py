from django.db import models

from apps.account_.models import Users
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

    total_rating = models.FloatField(default=0.0)
    rating_count = models.IntegerField(default=0)


class Medication_Rating(TimeStampedModel):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    medication = models.ForeignKey(Medications, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()

    def save(self, *args, **kwargs):
        medication = self.medication
        if self.pk is None:
            medication.total_rating = (
                medication.total_rating * medication.rating_count + self.rating
            ) / (medication.rating_count + 1)
            medication.rating_count += 1
        else:
            old_rating = Medication_Rating.objects.get(pk=self.pk).rating
            medication.total_rating = (
                medication.total_rating * medication.rating_count - old_rating + self.rating
            ) / medication.rating_count
        medication.save()
        super().save(*args, **kwargs)
