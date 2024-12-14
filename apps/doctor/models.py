from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from apps.account_.models import Users


class Doctors(models.Model):
    user = models.OneToOneField(
        Users,
        on_delete=models.CASCADE,
        related_name="doctor_profile"
    )
    specialization = models.CharField(max_length=100)
    experience_years = models.PositiveIntegerField()
    ratings = models.FloatField(
        validators=[
            MinValueValidator(1.0),
            MaxValueValidator(5.0)
        ],
        default=0.0
    )
    bio = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.full_name}"

class DoctorRating(models.Model):
    patient = models.ForeignKey(Users, on_delete=models.CASCADE, related_name="patient_ratings")
    doctor = models.ForeignKey(Doctors, on_delete=models.CASCADE, related_name="doctor_ratings")
    rating = models.FloatField(validators=[
        MinValueValidator(1.0),
        MaxValueValidator(5.0)
    ])
    # liked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('patient', 'doctor')

    def __str__(self):
        return f"{self.patient.full_name} -> {self.doctor.user.full_name} ({self.rating})"



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
