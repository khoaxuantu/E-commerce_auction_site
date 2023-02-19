# Generated by Django 4.1.6 on 2023-02-19 13:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_alter_product_image_path'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='auc_list',
        ),
        migrations.AlterField(
            model_name='product',
            name='seller',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='AuctionList',
        ),
    ]
