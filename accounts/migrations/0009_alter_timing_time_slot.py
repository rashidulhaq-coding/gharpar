# Generated by Django 4.0 on 2022-02-01 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_remove_shift_employee_shift_name_timing_shift'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timing',
            name='time_slot',
            field=models.TimeField(blank=True, null=True),
        ),
    ]