from django.contrib import admin

from apps.appointment.models import Appointments


@admin.register(Appointments)
class AppointmentsAdmin(admin.ModelAdmin):
    search_fields = ("id", "status", "confirmed", "created_at")
    list_display = ("id", "status", "confirmed", "created_at")
