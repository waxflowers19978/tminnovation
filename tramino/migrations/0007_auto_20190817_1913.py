# Generated by Django 2.1 on 2019-08-17 10:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tramino', '0006_auto_20190817_1834'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='eventpostcomment',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='eventpostcomment',
            name='updated_at',
        ),
        migrations.RemoveField(
            model_name='eventpostcomment',
            name='updated_by',
        ),
        migrations.AddField(
            model_name='eventpostcomment',
            name='guest_team_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='commenter_team', to='tramino.TeamInformations'),
        ),
    ]
