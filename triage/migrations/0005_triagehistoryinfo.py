# Generated by Django 4.2.17 on 2024-12-30 23:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('triage', '0004_alter_triagerecord_chief_symptom'),
    ]

    operations = [
        migrations.CreateModel(
            name='TriageHistoryInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('guahao_status', models.CharField(blank=True, choices=[('REGISTERED', '已挂号'), ('NOT_REGISTERED', '未挂号'), ('CANCELLED', '已退号')], max_length=20, null=True, verbose_name='挂号状态')),
                ('edit_triage', models.CharField(blank=True, choices=[('FIRST_TRIAGE', '初次分诊'), ('MODIFIED', '已修改'), ('SECOND_TRIAGE', '二次分诊')], default='FIRST_TRIAGE', max_length=20, null=True, verbose_name='修改状态')),
                ('departure_time', models.DateTimeField(blank=True, null=True, verbose_name='出科时间')),
                ('stay_duration', models.DurationField(blank=True, null=True, verbose_name='滞留急诊科时间')),
                ('assigned_doctor', models.ForeignKey(blank=True, limit_choices_to={'role': 'DOC'}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='doctor_triage_histories', to='triage.medicalstaff', verbose_name='责任医生')),
                ('assigned_nurse', models.ForeignKey(blank=True, limit_choices_to={'role': 'NUR'}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='nurse_triage_histories', to='triage.medicalstaff', verbose_name='责任护士')),
                ('triage_record', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='history_info', to='triage.triagerecord')),
            ],
            options={
                'verbose_name': 'Triage History Info',
                'verbose_name_plural': 'Triage History Info',
                'db_table': 'triage_history_info',
            },
        ),
    ]
