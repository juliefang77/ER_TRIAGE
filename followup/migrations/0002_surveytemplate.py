# Generated by Django 4.2.17 on 2025-01-05 23:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('triage', '0010_alter_vitalsigns_injury_position'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('followup', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SurveyTemplate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('survey_name', models.CharField(blank=True, max_length=100, null=True, verbose_name='模版名称')),
                ('uuid', models.UUIDField(blank=True, default=uuid.uuid4, editable=False, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='模版创建时间')),
                ('is_active', models.BooleanField(blank=True, default=True, null=True, verbose_name='是否启用')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='triage.medicalstaff', verbose_name='模版创建人')),
                ('hospital', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='医院')),
                ('question_1', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='template_question_1', to='followup.standardquestion', verbose_name='问题一')),
                ('question_2', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='template_question_2', to='followup.standardquestion', verbose_name='问题二')),
                ('question_3', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='template_question_3', to='followup.standardquestion', verbose_name='问题三')),
                ('question_4', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='template_question_4', to='followup.standardquestion', verbose_name='问题四')),
                ('question_5', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='template_question_5', to='followup.standardquestion', verbose_name='问题五')),
                ('question_6', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='template_question_6', to='followup.standardquestion', verbose_name='问题六')),
                ('question_7', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='template_question_7', to='followup.standardquestion', verbose_name='问题七')),
                ('question_8', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='template_question_8', to='followup.standardquestion', verbose_name='问题八')),
            ],
            options={
                'verbose_name': '随访问卷模版',
                'verbose_name_plural': '随访问卷模版',
            },
        ),
    ]
