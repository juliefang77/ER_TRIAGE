# Generated by Django 4.2.17 on 2025-02-06 06:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient_portal', '0017_patientuser_date_of_birth'),
    ]

    operations = [
        migrations.AddField(
            model_name='patientuser',
            name='username',
            field=models.CharField(blank=True, max_length=150, null=True, unique=True, verbose_name='用户名'),
        ),
    ]
