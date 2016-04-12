# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import login_token.models


class Migration(migrations.Migration):

    dependencies = [
        ('instances', '0002_auto_20151001_1132'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='LoginToken',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('token', models.TextField(default=login_token.models.generate_token, unique=True, max_length=255)),
                ('instance', models.ForeignKey(verbose_name='instance', to='instances.Instance')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
