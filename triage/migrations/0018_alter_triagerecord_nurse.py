# Generated by Django 4.2.17 on 2025-01-25 18:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('triage', '0017_massinjury_hospital'),
    ]

    operations = [
        migrations.AlterField(
            model_name='triagerecord',
            name='nurse',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='分诊护士'),
        ),
    ]
