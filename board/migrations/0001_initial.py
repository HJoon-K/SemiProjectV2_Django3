# Generated by Django 3.2.13 on 2022-07-01 15:54

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('join', '0008_alter_member_userid'),
    ]

    operations = [
        migrations.CreateModel(
            name='Board',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.TextField()),
                ('regdate', models.DateTimeField(default=datetime.datetime.now)),
                ('thumbup', models.IntegerField(default=0)),
                ('views', models.IntegerField(default=0)),
                ('contents', models.TextField()),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='join.member')),
            ],
            options={
                'db_table': 'board',
            },
        ),
    ]
