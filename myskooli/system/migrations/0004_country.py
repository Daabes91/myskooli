# Generated by Django 2.0.1 on 2020-02-23 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0003_delete_country'),
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country_name', models.CharField(max_length=60)),
                ('country_img', models.CharField(default=None, max_length=600)),
            ],
        ),
    ]
