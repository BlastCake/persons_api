# Generated by Django 2.2.7 on 2019-11-14 12:28

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20191112_1134'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='vector',
            field=django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(), size=None), blank=True, default=list, size=5),
        ),
    ]
