# Generated by Django 4.2.17 on 2025-01-09 05:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('followup', '0012_remove_surveytemplate_submitted_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='followuprecipient',
            name='phone',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='联系电话'),
        ),
        migrations.AddField(
            model_name='followuprecipient',
            name='research_patient',
            field=models.BooleanField(blank=True, null=True, verbose_name='重要随访对象'),
        ),
    ]
