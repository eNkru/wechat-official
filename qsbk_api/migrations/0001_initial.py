# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Joke',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('author', models.CharField(max_length=50)),
                ('content', models.CharField(max_length=255)),
                ('like', models.CharField(max_length=10)),
            ],
        ),
    ]
