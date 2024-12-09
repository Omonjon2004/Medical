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
    ratings = models.FloatField(validators=[
        MinValueValidator(1.0),
        MaxValueValidator(5.0)
    ])
    bio = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.full_name}"



class AppointmentSlot(models.Model):
    doctor = models.ForeignKey('Doctors', on_delete=models.CASCADE, related_name='appointment_slots')
    date = models.DateField()
    time = models.TimeField()
    is_available = models.BooleanField(default=True)

    class Meta:
        unique_together = ('doctor', 'date', 'time')

    def __str__(self):
        return f'{self.date} {self.time} - {self.is_available}'


class Appointment(models.Model):
    patient = models.ForeignKey(
        Users,
        on_delete=models.CASCADE,
        related_name="patient_appointments"
    )
    doctor = models.ForeignKey(
        Doctors,
        on_delete=models.CASCADE,
        related_name="doctor_appointments"
    )
    slot = models.OneToOneField(
        AppointmentSlot,
        on_delete=models.CASCADE,
        related_name="slot_appointment"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Appointment with Dr. {self.doctor.user.last_name} at {self.slot.time} on {self.slot.date}"
