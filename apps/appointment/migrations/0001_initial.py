# Generated by Django 5.1.3 on 2024-12-11 11:16

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('doctor', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Appointments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('Upcoming', 'Upcoming'), ('Completed', 'Completed'), ('Canceled', 'Canceled')], default='Upcoming', max_length=20)),
                ('confirmed', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='doctor_appointments', to='doctor.doctors')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='patient_appointments', to=settings.AUTH_USER_MODEL)),
                ('slot', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='slot_appointment', to='doctor.appointmentslot')),
            ],
            options={
                'constraints': [models.UniqueConstraint(fields=('doctor', 'slot'), name='unique_doctor_slot')],
            },
        ),
    ]