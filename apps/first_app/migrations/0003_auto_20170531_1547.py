# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-31 20:47
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('first_app', '0002_employee_password'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Employee',
            new_name='User',
        ),
        migrations.RenameField(
            model_name='clock_in',
            old_name='employee',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='clock_out',
            old_name='employee',
            new_name='user',
        ),
    ]