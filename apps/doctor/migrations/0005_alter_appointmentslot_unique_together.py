# Generated by Django 5.1.3 on 2024-12-15 06:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0004_alter_appointmentslot_unique_together'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='appointmentslot',
            unique_together={('doctor', 'date', 'time')},
        ),
    ]
