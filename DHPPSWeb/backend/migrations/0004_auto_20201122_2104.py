# Generated by Django 3.1.3 on 2020-11-22 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0003_auto_20201122_1955'),
    ]

    operations = [
        migrations.AlterField(
            model_name='PersonalProfile',
            name='avatar',
            field=models.ImageField(default='defaultFiles/defaultAvatar.png', upload_to='avatar', verbose_name='头像'),
        ),
    ]
