# Generated by Django 4.2.17 on 2025-01-08 05:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient_portal', '0009_alter_patienttriagesubmission_hospital'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patientuser',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
