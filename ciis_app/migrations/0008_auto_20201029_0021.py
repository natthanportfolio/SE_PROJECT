# Generated by Django 3.1.1 on 2020-10-28 17:21

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('ciis_app', '0007_userap'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='userap',
            managers=[
                ('object', django.db.models.manager.Manager()),
            ],
        ),
    ]
