# Generated by Django 3.1.7 on 2021-03-18 11:19

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('se_app', '0013_auto_20210316_0926'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_details',
            name='first_name',
            field=models.CharField(default=django.utils.timezone.now, max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user_details',
            name='last_name',
            field=models.CharField(default=django.utils.timezone.now, max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='card_details',
            name='autographed',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]
