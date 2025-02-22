# Generated by Django 4.2.17 on 2025-01-08 08:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('patient_portal', '0010_alter_patientuser_id'),
        ('triage', '0010_alter_vitalsigns_injury_position'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='patient_user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='patient_portal.patientuser', verbose_name='患者账号'),
        ),
    ]
