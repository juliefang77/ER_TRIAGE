# Generated by Django 4.2.17 on 2025-01-15 03:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('followup', '0025_followupmessage_template'),
    ]

    operations = [
        migrations.AlterField(
            model_name='followuprecipient',
            name='message_reply',
            field=models.CharField(blank=True, choices=[('WEEKEND', '周末'), ('WEEK_DAY', '周中白天'), ('WEEK_NIGHT', '周中晚上'), ('ANYTIME', '任意时间'), ('SENT', '已发送未回复'), ('NOT_SENT', '未发送')], default='NOT_SENT', max_length=20, null=True, verbose_name='回复时间偏好'),
        ),
        migrations.AlterField(
            model_name='followuprecipient',
            name='survey_status',
            field=models.CharField(blank=True, choices=[('NOT_SENT', '未发送'), ('NO_RESPONSE', '已发送未完成'), ('YES_RESPONSE', '已完成')], default='NOT_SENT', max_length=20, null=True, verbose_name='问卷状态'),
        ),
    ]
