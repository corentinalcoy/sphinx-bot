# Generated by Django 2.2.7 on 2019-11-22 23:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_auto_20191122_2325'),
    ]

    operations = [
        migrations.AddField(
            model_name='connector',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
