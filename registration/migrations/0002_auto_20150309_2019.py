# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='aboutMe',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='avatar',
            field=models.FileField(null=True, upload_to=b'profile/'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='interests',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
