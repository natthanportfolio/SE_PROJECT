# Generated by Django 3.1.1 on 2020-10-28 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ciis_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='userap',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('firstname', models.CharField(max_length=255)),
                ('lastname', models.CharField(max_length=255)),
                ('phoneno', models.CharField(max_length=255)),
                ('passportid', models.CharField(max_length=255)),
                ('affiliation', models.CharField(max_length=255)),
                ('country', models.CharField(max_length=255)),
                ('nationality', models.CharField(max_length=255)),
                ('status', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254)),
                ('password', models.CharField(max_length=255)),
            ],
        ),
    ]
