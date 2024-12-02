from django.utils import timezone
from django.db import models

from apps.dockot.models import Doctors
from apps.patient.models import Patients
from apps.shared.models import TimeStampedModel


# Create your models here.

class Appointments(TimeStampedModel):
    patient_id = models.ForeignKey(Patients, on_delete=models.CASCADE)
    doctor_id = models.ForeignKey(Doctors, on_delete=models.CASCADE)
    appointment_date = models.DateField()
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('COMPLETED', 'Completed'),
        ('CANCELED', 'Canceled')
    )
    status = models.CharField(max_length=10,
                              choices=STATUS_CHOICES, default='PENDING')
    notes = models.TextField()


class Payments(TimeStampedModel):
    patient_id = models.ForeignKey(Patients, on_delete=models.CASCADE)
    appointment_id = models.ForeignKey(Appointments, on_delete=models.CASCADE)
    amount = models.FloatField()
    payment_date = timezone.now()
    STATUS_CHOICES = (
        ('PAID', 'Paid'),
        ('PENDING', 'Pending'),
        ('FAILED', 'Failed'),
    )
