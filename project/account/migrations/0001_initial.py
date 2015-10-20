# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Domain',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text=b'Domain Name', unique=True, max_length=253)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='Organisation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=32, verbose_name=b'Organisation Name')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.AddField(
            model_name='membership',
            name='organisation',
            field=models.ForeignKey(related_name='members', to='account.Organisation'),
        ),
        migrations.AddField(
            model_name='membership',
            name='user',
            field=models.ForeignKey(related_name='organisations', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='domain',
            name='organisation',
            field=models.ForeignKey(related_name='domains', to='account.Organisation'),
        ),
        migrations.AlterUniqueTogether(
            name='membership',
            unique_together=set([('user', 'organisation')]),
        ),
    ]
