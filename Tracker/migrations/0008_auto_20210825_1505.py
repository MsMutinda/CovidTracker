# Generated by Django 3.2.6 on 2021-08-25 12:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Tracker', '0007_alter_health_active_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='health',
            old_name='active_user',
            new_name='is_active',
        ),
        migrations.RenameField(
            model_name='travel',
            old_name='active_user',
            new_name='is_active',
        ),
    ]
