# Generated by Django 3.1.7 on 2021-03-12 12:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('se_app', '0004_auto_20210312_1232'),
    ]

    operations = [
        migrations.RenameField(
            model_name='autograde',
            old_name='grade_name',
            new_name='auto_grade',
        ),
        migrations.RenameField(
            model_name='card_category',
            old_name='category_name',
            new_name='sports',
        ),
        migrations.RenameField(
            model_name='card_details',
            old_name='grade_name',
            new_name='auto_grade',
        ),
        migrations.RenameField(
            model_name='card_details',
            old_name='card_grade_name',
            new_name='card_grade',
        ),
        migrations.RenameField(
            model_name='cardgrade',
            old_name='card_grade_name',
            new_name='card_grade',
        ),
        migrations.RenameField(
            model_name='certifications',
            old_name='certificate_name',
            new_name='certificates',
        ),
    ]
