# Generated by Django 2.1 on 2019-08-14 06:23

from django.db import migrations
import imagekit.models.fields
import tramino.models


class Migration(migrations.Migration):

    dependencies = [
        ('tramino', '0002_auto_20190814_1406'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teaminformations',
            name='commander_picture',
            field=imagekit.models.fields.ProcessedImageField(default='SOME STRING', upload_to=tramino.models.get_commander),
        ),
    ]
