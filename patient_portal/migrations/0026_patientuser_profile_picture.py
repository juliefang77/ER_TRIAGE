# Generated by Django 4.2.17 on 2025-02-14 07:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient_portal', '0025_bookingpayment_patient_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='patientuser',
            name='profile_picture',
            field=models.IntegerField(blank=True, null=True, verbose_name='头像'),
        ),
    ]
