# Generated by Django 3.1.7 on 2021-03-11 11:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('se_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user_details',
            name='is_staff',
        ),
    ]
