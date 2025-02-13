# Generated by Django 4.2.17 on 2025-02-03 03:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('followup', '0032_alter_bookingonline_hospital_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookingonline',
            name='actual_time',
            field=models.DateTimeField(blank=True, help_text='完成或取消时的实际时间', null=True, verbose_name='实际完成/取消时间'),
        ),
        migrations.AlterField(
            model_name='bookingonline',
            name='status',
            field=models.CharField(blank=True, choices=[('PATIENT_SUBMITTED', '患者已下单'), ('HOSPITAL_ACCEPTED', '医院已接受订单'), ('CONSULTATION_COMPLETED', '问诊已完成'), ('CANCELLED', '医院已拒绝')], default='PATIENT_SUBMITTED', max_length=50, null=True, verbose_name='订单状态'),
        ),
    ]
