# Generated by Django 4.0.3 on 2022-05-10 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_orderservice_delete_orderitem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='package',
            name='discount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Discount'),
        ),
    ]
