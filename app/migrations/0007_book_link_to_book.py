# Generated by Django 4.2.7 on 2023-12-11 19:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_alter_student_registration_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='link_to_book',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Kitob havolasi'),
        ),
    ]
