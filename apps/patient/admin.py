from django.contrib import admin

from apps.patient.models import Patients


@admin.register(Patients)
class PatientsAdmin(admin.ModelAdmin):
    list_display = ("id",
                    "user_id",
                    "age",
                    "gender",
                    "medical_history",
                    "additional_phone_number"
                    )
    search_fields = ("id",
                     "age",
                     "gender",
                     "medical_history",
                     "additional_phone_number"
                     )
