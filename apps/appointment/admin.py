from django.contrib import admin

from apps.appointment.models import Appointments


class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'slot', 'patient', 'status', 'confirmed', 'created_at')
    search_fields = ('doctor__user__full_name', 'patient__user__full_name')

admin.site.register(Appointments, AppointmentAdmin)
