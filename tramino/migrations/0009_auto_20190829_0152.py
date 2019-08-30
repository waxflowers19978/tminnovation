# Generated by Django 2.1 on 2019-08-28 16:52

from django.db import migrations, models
import imagekit.models.fields
import tramino.models


class Migration(migrations.Migration):

    dependencies = [
        ('tramino', '0008_auto_20190818_1946'),
    ]

    operations = [
        migrations.AddField(
            model_name='teaminformations',
            name='activity_place_picture',
            field=imagekit.models.fields.ProcessedImageField(default='SOME STRING', upload_to=tramino.models.get_activity_place_pic),
        ),
        migrations.AddField(
            model_name='teaminformations',
            name='address',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='teaminformations',
            name='achievement',
            field=models.CharField(blank=True, choices=[['全国大会優勝レベル', '全国大会優勝レベル'], ['全国大会入賞レベル', '全国大会入賞レベル'], ['全国大会出場常連レベル', '全国大会出場常連レベル'], ['全国大会出場レベル', '全国大会出場レベル'], ['都道府県大会入賞レベル', '都道府県大会入賞レベル'], ['都道府県大会常連レベル', '都道府県大会常連レベル'], ['都道府県大会出場レベル', '都道府県大会出場レベル'], ['地区大会入賞レベル', '地区大会入賞レベル'], ['地区大会常連レベル', '地区大会常連レベル']], max_length=30, null=True),
        ),
    ]