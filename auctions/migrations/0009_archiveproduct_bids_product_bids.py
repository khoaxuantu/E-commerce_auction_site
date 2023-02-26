# Generated by Django 4.1.6 on 2023-02-26 18:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_alter_archiveproduct_table'),
    ]

    operations = [
        migrations.AddField(
            model_name='archiveproduct',
            name='bids',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='product',
            name='bids',
            field=models.PositiveIntegerField(default=0),
        ),
    ]