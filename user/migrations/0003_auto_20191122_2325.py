# Generated by Django 2.2.7 on 2019-11-22 23:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20191122_2325'),
    ]

    operations = [
        migrations.AlterField(
            model_name='githubuser',
            name='type',
            field=models.CharField(choices=[('organization', 'organization'), ('user', 'user'), ('enterprise', 'enterprise')], default='user', max_length=20),
        ),
    ]
