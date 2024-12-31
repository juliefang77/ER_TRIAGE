# Generated by Django 4.2.17 on 2024-12-30 23:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('triage', '0005_triagehistoryinfo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vitalsigns',
            name='injury_position',
            field=models.CharField(blank=True, choices=[('LIMBS_SKIN', '四肢/皮肤'), ('BACK', '背部'), ('CHEST', '胸部'), ('ABDOMEN', '腹部'), ('HEAD_NECK', '头颈部'), ('BUTTOCKS', '臀部')], max_length=100, null=True, verbose_name='损伤部位'),
        ),
        migrations.AlterField(
            model_name='vitalsigns',
            name='injury_type',
            field=models.CharField(blank=True, choices=[('LACERATION', '裂伤/挫伤'), ('STAB', '刺伤'), ('BLUNT', '钝性伤'), ('GUNSHOT', '弹道伤'), ('BURN', '烧伤')], max_length=20, null=True, verbose_name='损伤类型'),
        ),
    ]
