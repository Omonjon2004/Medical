# Generated by Django 5.1.3 on 2024-12-03 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_remove_users_avatar'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='full_name',
            field=models.CharField(default=2, max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='users',
            name='password',
            field=models.CharField(max_length=255),
        ),
    ]
