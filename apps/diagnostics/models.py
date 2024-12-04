from django.db import models

from apps.doctor.models import Doctors
from apps.patient.models import Patients
from apps.shared.models import TimeStampedModel


# Create your models here.
class Medical_Records(TimeStampedModel):
    patient_id = models.ForeignKey(Patients, on_delete=models.CASCADE)
    doctor_id = models.ForeignKey(Doctors, on_delete=models.CASCADE)
    record_date = models.DateField()
    description = models.TextField()
    attachments = models.CharField(max_length=255)


class Prescriptions(TimeStampedModel):
    medical_record_id = models.ForeignKey(Medical_Records,
                                          on_delete=models.CASCADE)
    medication_name = models.CharField(max_length=255)
    dosage = models.CharField(max_length=255)
    instructions = models.CharField(max_length=255)
