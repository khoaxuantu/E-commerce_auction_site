# Generated by Django 4.1.6 on 2023-02-18 16:28

import auctions.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image_path',
            field=models.ImageField(upload_to=auctions.models.user_directory_path, verbose_name='Image path'),
        ),
    ]