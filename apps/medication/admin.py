from django.contrib import admin

from apps.medication.models import Medications


@admin.register(Medications)
class MedicationsAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description", "dosage_form", "strength", "price", "stock_quantity", "manufacturer")
    search_fields = ("id", "name", "description", "strength", "price", "stock_quantity", "manufacturer")