# Generated by Django 4.2.7 on 2023-11-16 19:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_alter_student_course'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='registration_date',
            field=models.DateField(blank=True, null=True, verbose_name="Ro'yxatga olingan sana"),
        ),
    ]
