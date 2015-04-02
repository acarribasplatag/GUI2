# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('polls', '0002_category_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='NegativeVote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pub_date', models.DateTimeField(verbose_name=b'date published')),
                ('choice', models.ForeignKey(to='polls.Choice')),
                ('poll', models.ForeignKey(to='polls.Poll')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='vote',
            name='old',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
