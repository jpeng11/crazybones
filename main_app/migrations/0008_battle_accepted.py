# Generated by Django 3.0.7 on 2020-07-08 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0007_battle'),
    ]

    operations = [
        migrations.AddField(
            model_name='battle',
            name='accepted',
            field=models.BooleanField(default=False),
        ),
    ]
