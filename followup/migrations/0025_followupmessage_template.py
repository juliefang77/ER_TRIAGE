# Generated by Django 4.2.17 on 2025-01-15 02:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('followup', '0024_messagetemplate'),
    ]

    operations = [
        migrations.AddField(
            model_name='followupmessage',
            name='template',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='followup.messagetemplate', verbose_name='消息模版'),
        ),
    ]
