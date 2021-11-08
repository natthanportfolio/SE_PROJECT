# Generated by Django 3.1.1 on 2020-11-03 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ciis_app', '0034_remove_paymentpaper_last_payment'),
    ]

    operations = [
        migrations.CreateModel(
            name='Memberparticipant',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('banquet', models.IntegerField()),
                ('paperlist', models.CharField(max_length=255)),
                ('user', models.CharField(max_length=255)),
                ('price', models.IntegerField()),
                ('person', models.IntegerField()),
                ('datebill', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(max_length=255)),
                ('userfirstname', models.CharField(max_length=255)),
                ('userlastname', models.CharField(max_length=255)),
                ('userpassport', models.CharField(max_length=255)),
                ('userphone', models.CharField(max_length=255)),
                ('firstname1', models.CharField(max_length=255)),
                ('lastname1', models.CharField(max_length=255)),
                ('email1', models.CharField(max_length=255)),
                ('firstname2', models.CharField(max_length=255)),
                ('lastname2', models.CharField(max_length=255)),
                ('email2', models.CharField(max_length=255)),
                ('firstname3', models.CharField(max_length=255)),
                ('lastname3', models.CharField(max_length=255)),
                ('email3', models.CharField(max_length=255)),
                ('firstname4', models.CharField(max_length=255)),
                ('lastname4', models.CharField(max_length=255)),
                ('email4', models.CharField(max_length=255)),
                ('firstname5', models.CharField(max_length=255)),
                ('lastname5', models.CharField(max_length=255)),
                ('email5', models.CharField(max_length=255)),
            ],
        ),
    ]
