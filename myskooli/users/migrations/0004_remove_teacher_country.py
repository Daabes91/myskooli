# Generated by Django 2.0.1 on 2020-02-23 13:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20200223_1406'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teacher',
            name='country',
        ),
    ]
