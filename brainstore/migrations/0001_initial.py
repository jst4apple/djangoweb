# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-01-28 13:37
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Connect',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Edge',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('call', models.CharField(max_length=64)),
                ('called', models.CharField(max_length=64)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Node',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='connect',
            name='edge',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='brainstore.Edge'),
        ),
        migrations.AddField(
            model_name='connect',
            name='entityend',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='node_end', to='brainstore.Node'),
        ),
        migrations.AddField(
            model_name='connect',
            name='entitystart',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='node_start', to='brainstore.Node'),
        ),
    ]
