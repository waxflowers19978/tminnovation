# Generated by Django 2.1 on 2019-08-06 08:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tramino', '0004_auto_20190806_1724'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventApplyPool',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='EventPostPool',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_name', models.CharField(max_length=50)),
                ('event_description', models.CharField(max_length=300)),
                ('event_date', models.DateField(verbose_name='date published')),
                ('apply_deadline', models.DateField(verbose_name='date published')),
                ('event_host_team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='event_posts', to='tramino.TeamInformations')),
            ],
        ),
        migrations.CreateModel(
            name='FavoriteEventPool',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_post_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='event_favorites', to='tramino.EventPostPool')),
                ('guest_team_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='event_favorites', to='tramino.TeamInformations')),
            ],
        ),
        migrations.CreateModel(
            name='FavoriteTeamPool',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('guest_team_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorite_recipient_team', to='tramino.TeamInformations')),
                ('host_team_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorite_sender_team', to='tramino.TeamInformations')),
            ],
        ),
        migrations.CreateModel(
            name='PastGameRecords',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('opponent_team_name', models.CharField(max_length=50)),
                ('game_category', models.CharField(choices=[['練習試合', '練習試合'], ['公式戦', '公式戦']], max_length=30)),
                ('my_score', models.CharField(choices=[['0', '0'], ['1', '1'], ['2', '2'], ['3', '3'], ['4', '4'], ['5', '5'], ['6', '6'], ['7', '7'], ['8', '8'], ['9', '9'], ['10', '10'], ['11~', '11~']], max_length=30)),
                ('opponent_score', models.CharField(choices=[['0', '0'], ['1', '1'], ['2', '2'], ['3', '3'], ['4', '4'], ['5', '5'], ['6', '6'], ['7', '7'], ['8', '8'], ['9', '9'], ['10', '10'], ['11~', '11~']], max_length=30)),
                ('game_data', models.DurationField(verbose_name='date published')),
                ('game_description', models.CharField(blank=True, max_length=300, null=True)),
                ('register_team_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='past_game_records', to='tramino.TeamInformations')),
            ],
        ),
        migrations.AddField(
            model_name='eventapplypool',
            name='event_post_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='event_applies', to='tramino.EventPostPool'),
        ),
        migrations.AddField(
            model_name='eventapplypool',
            name='guest_team_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='event_applies', to='tramino.TeamInformations'),
        ),
    ]
