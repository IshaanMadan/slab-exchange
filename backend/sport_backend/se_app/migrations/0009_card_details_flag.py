# Generated by Django 3.1.7 on 2021-03-15 07:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('se_app', '0008_user_details_is_staff'),
    ]

    operations = [
        migrations.AddField(
            model_name='card_details',
            name='flag',
            field=models.BooleanField(default=False, null=True),
        ),
    ]