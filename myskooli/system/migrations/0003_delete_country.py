# Generated by Django 2.0.1 on 2020-02-23 13:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_remove_teacher_country'),
        ('system', '0002_country'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Country',
        ),
    ]
