# Generated by Django 2.1.3 on 2020-02-12 16:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=60)),
                ('category_img', models.CharField(default=None, max_length=600)),
            ],
        ),
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subcategory_name', models.CharField(max_length=60)),
                ('subcategory_img', models.CharField(default=None, max_length=600)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='system.Category')),
            ],
        ),
    ]
