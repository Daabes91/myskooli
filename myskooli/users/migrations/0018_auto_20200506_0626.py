# Generated by Django 3.0.4 on 2020-05-06 03:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0005_auto_20200229_1610'),
        ('users', '0017_auto_20200312_1456'),
    ]

    operations = [
        migrations.AlterField(
            model_name='packagelessons',
            name='number_of_lessons',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='subcategory',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='system.SubCategory'),
        ),
    ]
