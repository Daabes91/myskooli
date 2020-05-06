# Generated by Django 2.0.1 on 2020-02-23 16:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_auto_20200223_1720'),
    ]

    operations = [
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Student')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Teacher')),
            ],
        ),
        migrations.AddField(
            model_name='reviews',
            name='rate',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
