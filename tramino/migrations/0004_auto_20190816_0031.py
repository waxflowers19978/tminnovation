# Generated by Django 2.1 on 2019-08-15 15:31

from django.db import migrations
import imagekit.models.fields
import tramino.models


class Migration(migrations.Migration):

    dependencies = [
        ('tramino', '0003_auto_20190814_1523'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teaminformations',
            name='team_picture',
            field=imagekit.models.fields.ProcessedImageField(default='SOME STRING', upload_to=tramino.models.get_team),
        ),
    ]
