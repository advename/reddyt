# Generated by Django 3.0.6 on 2020-05-12 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discussion_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='votes',
            field=models.IntegerField(default=0),
        ),
    ]
