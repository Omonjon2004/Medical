from django.contrib import admin

from apps.account_.models import Users
from apps.doctor.models import Doctors


class DoctorTabularInline(admin.TabularInline):
    model = Doctors
    extra = 1


@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    inlines = [DoctorTabularInline]
    search_fields = ('id',
                     'full_name',
                     'email')
    list_display = ('id',
                    'full_name',
                    'email',
                    'is_active',
                    'is_staff')
