# Generated by Django 5.1.2 on 2024-12-30 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='show',
            name='watcher',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='show',
            name='hour_show',
            field=models.IntegerField(choices=[(8, '8h'), (9, '9h'), (13, '13h'), (18, '18h'), (20, '20h')]),
        ),
    ]
