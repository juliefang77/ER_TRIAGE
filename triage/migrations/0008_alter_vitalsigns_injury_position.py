# Generated by Django 4.2.17 on 2025-01-01 00:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('triage', '0007_alter_medicalstaff_role_alter_medicalstaff_staff_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vitalsigns',
            name='injury_position',
            field=models.JSONField(blank=True, default=list, null=True, verbose_name='损伤部位'),
        ),
    ]
