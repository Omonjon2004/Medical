from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from apps.account_.models import Users
from apps.shared.models import TimeStampedModel


class Doctors(TimeStampedModel):
    user = models.OneToOneField(
        Users,
        on_delete=models.CASCADE,
        related_name="doctor_profile"
    )
    specialization = models.CharField(max_length=100)
    experience_years = models.PositiveIntegerField()
    bio = models.TextField()

    total_rating = models.FloatField(default=0.0)
    rating_count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.full_name}"


class Doctor_Rating(TimeStampedModel):
    user = models.ForeignKey(
        Users,
        on_delete=models.CASCADE,
        related_name="doctor_ratings"
    )
    doctor = models.ForeignKey(
        Doctors,
        on_delete=models.CASCADE,
        related_name="ratings"
    )
    rating = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ]
    )

    def save(self, *args, **kwargs):
        doctor = self.doctor
        if self.pk is None:
            doctor.total_rating = (
                doctor.total_rating * doctor.rating_count + self.rating
            ) / (doctor.rating_count + 1)
            doctor.rating_count += 1
        else:
            old_rating = Doctor_Rating.objects.get(pk=self.pk).rating
            doctor.total_rating = (
                doctor.total_rating * doctor.rating_count - old_rating + self.rating
            ) / doctor.rating_count
        doctor.save()
        super().save(*args, **kwargs)


class AppointmentSlot(models.Model):
    doctor = models.ForeignKey('Doctors',
                               on_delete=models.CASCADE,
                               related_name='appointment_slots')
    date = models.DateField()
    time = models.TimeField()
    is_available = models.BooleanField(default=True)

    class Meta:
        unique_together = ('doctor', 'date', 'time')

    def __str__(self):
        return f'{self.date} {self.time} - {self.is_available}'


