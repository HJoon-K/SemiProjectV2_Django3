# Generated by Django 3.2.13 on 2022-06-29 15:28

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('join', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='addr',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='member',
            name='email',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='member',
            name='mailing',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='member',
            name='name',
            field=models.CharField(default='', max_length=7),
        ),
        migrations.AddField(
            model_name='member',
            name='passwd',
            field=models.CharField(default='', max_length=18),
        ),
        migrations.AddField(
            model_name='member',
            name='phone',
            field=models.CharField(default='', max_length=15),
        ),
        migrations.AddField(
            model_name='member',
            name='regdate',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name='member',
            name='userid',
            field=models.CharField(default='', max_length=18),
        ),
        migrations.AddField(
            model_name='member',
            name='zipcode',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.DO_NOTHING, to='join.zipcode'),
        ),
        migrations.AlterField(
            model_name='member',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterModelTable(
            name='member',
            table='member',
        ),
    ]