# Generated by Django 4.2.17 on 2025-01-22 22:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('triage', '0013_hospitaluser_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='id_system',
            field=models.AutoField(primary_key=True, serialize=False, verbose_name='唯一标识'),
        ),
    ]
