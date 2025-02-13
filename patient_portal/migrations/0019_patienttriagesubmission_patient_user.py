# Generated by Django 4.2.17 on 2025-02-06 06:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('patient_portal', '0018_patientuser_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='patienttriagesubmission',
            name='patient_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='triage_submissions', to='patient_portal.patientuser', verbose_name='患者用户'),
        ),
    ]
