# Generated by Django 4.2.17 on 2025-01-15 04:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('triage', '0012_alter_patient_patient_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='hospitaluser',
            name='name',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='医院用户名称'),
        ),
    ]
