# Generated by Django 4.2.7 on 2023-12-17 19:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_book_link_to_book'),
    ]

    operations = [
        migrations.CreateModel(
            name='TelegramUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('telegram_id', models.IntegerField(unique=True, verbose_name='Telegram ID')),
                ('firstname', models.CharField(max_length=255, verbose_name='Ismi')),
                ('lastname', models.CharField(max_length=255, verbose_name='Familiyasi')),
                ('username', models.CharField(blank=True, max_length=255, null=True, verbose_name='Username')),
                ('phone', models.CharField(blank=True, max_length=255, null=True, verbose_name='Telefon raqami')),
                ('lang_code', models.CharField(blank=True, max_length=255, null=True, verbose_name='Til kodi')),
                ('passport', models.CharField(blank=True, max_length=255, null=True, verbose_name='Passport seriyasi')),
            ],
            options={
                'verbose_name': 'Telegram foydalanuvchisi',
                'verbose_name_plural': 'Telegram foydalanuvchilar',
                'db_table': 'telegram_users',
                'ordering': ['telegram_id', 'passport'],
            },
        ),
    ]
