# Generated by Django 4.2.17 on 2025-01-25 22:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('triage', '0021_alter_triageresult_treatment_area'),
    ]

    operations = [
        migrations.AlterField(
            model_name='massinjury',
            name='hospital',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='mass_injuries', to='triage.hospital', verbose_name='所属医院'),
        ),
        migrations.AlterField(
            model_name='medicalstaff',
            name='hospital',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='staff', to='triage.hospital', verbose_name='所属医院'),
        ),
        migrations.AlterField(
            model_name='triagerecord',
            name='hospital',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='triage_records', to='triage.hospital', verbose_name='所属医院'),
        ),
    ]
