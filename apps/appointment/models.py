from django.db import models

from apps.account_.models import Users
from apps.doctor.models import Doctors, AppointmentSlot


class Appointments(models.Model):
    STATUS_CHOICES = [
        ('Upcoming', 'Upcoming'),
        ('Completed', 'Completed'),
        ('Canceled', 'Canceled'),
    ]
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
    patient = models.ForeignKey(
        Users,
        on_delete=models.CASCADE,
        related_name='patient_appointments'
    )

    status = models.CharField(max_length=20,
                              choices=STATUS_CHOICES,
                              default='Upcoming'
                              )
    confirmed = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['doctor', 'slot'],
                name='unique_doctor_slot'
            )
        ]

    def __str__(self):
        return (f"Appointment with Dr. "
                f"{self.doctor.user.full_name}"
                f" on {self.slot.date} at "
                f"{self.slot.time}")
