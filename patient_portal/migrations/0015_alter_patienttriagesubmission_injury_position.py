# Generated by Django 4.2.17 on 2025-01-28 04:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient_portal', '0014_alter_patienttriagesubmission_id_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patienttriagesubmission',
            name='injury_position',
            field=models.CharField(blank=True, choices=[('L', '四肢/皮肤'), ('B', '背部'), ('C', '胸部'), ('A', '腹部'), ('H', '头颈部'), ('P', '臀部')], max_length=255, null=True, verbose_name='小人图/损伤部位'),
        ),
    ]
