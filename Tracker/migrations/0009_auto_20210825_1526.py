# Generated by Django 3.2.6 on 2021-08-25 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Tracker', '0008_auto_20210825_1505'),
    ]

    operations = [
        migrations.AlterField(
            model_name='health',
            name='is_active',
            field=models.BooleanField(default=None),
        ),
        migrations.AlterField(
            model_name='travel',
            name='is_active',
            field=models.BooleanField(default=None),
        ),
    ]
