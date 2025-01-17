# Generated by Django 4.2.17 on 2025-01-17 03:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('followup', '0027_followupmessage_responded_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='SurveyAi',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='分析时间')),
                ('analysis_name', models.CharField(blank=True, max_length=100, null=True, verbose_name='AI稿件名称')),
                ('analysis_result', models.TextField(blank=True, null=True, verbose_name='AI分析结果')),
                ('hospital', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='医院')),
                ('recipients', models.ManyToManyField(blank=True, related_name='survey_analyses', to='followup.followuprecipient', verbose_name='分析的患者')),
            ],
            options={
                'verbose_name': '问卷AI分析结果',
                'verbose_name_plural': '问卷AI分析结果',
                'ordering': ['-created_at'],
            },
        ),
    ]
