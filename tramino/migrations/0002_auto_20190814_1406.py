# Generated by Django 2.1 on 2019-08-14 05:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tramino', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teaminformations',
            name='achievement',
            field=models.CharField(blank=True, choices=[['全国大会優勝レベル', '全国大会優勝レベル'], ['全国大会入賞レベル', '全国大会入賞レベル'], ['全国大会出場常連レベル', '全国大会出場常連レベル'], ['全国大会出場レベル', '全国大会出場レベル'], ['都道府県大会入賞レベル', '都道府県大会入賞レベル'], ['都道府県大会常連レベル', '都道府県大会常連レベル'], ['都道府県大会出場レベル', '都道府県 大会出場レベル'], ['地区大会入賞レベル', '地区大会入賞レベル'], ['地区大会常連レベル', '地区大会常連レベル']], max_length=30, null=True),
        ),
    ]
