from django.db import models

from apps.account_.models import Users
from apps.medication.models import Medications
from apps.shared.models import TimeStampedModel


# Create your models here.


class Orders(TimeStampedModel):
    user_id = models.ForeignKey(Users,
                                on_delete=models.CASCADE)
    total_amount = models.FloatField()
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('SHIPPED', 'SHipped'),
        ('DELIVERED', 'Delivered'),
        ('CANCELLED', 'Cancelled')
    )


class OrderItems(TimeStampedModel):
    order_id = models.ForeignKey(Orders,
                                 on_delete=models.CASCADE)
    medication_id = models.ForeignKey(Medications,
                                      on_delete=models.CASCADE)
    quantity = models.FloatField()
    price_per_unit = models.FloatField()
    subtotal = models.FloatField()
