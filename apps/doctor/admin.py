from django.contrib import admin

from apps.doctor.models import Doctors, AppointmentSlot


class AppointmentSlotTabularInline(admin.TabularInline):
    model = AppointmentSlot
    extra = 1


@admin.register(Doctors)
class DoctorsAdmin(admin.ModelAdmin):
    inlines = [AppointmentSlotTabularInline]
    search_fields = (
        'id',
        "specialization",
        'experience_years',
        'user__full_name',
    )
    list_display = ('id',
                    'user',
                    'specialization',
                    'experience_years',

                    )
