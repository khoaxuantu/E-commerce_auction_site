# Generated by Django 4.1.6 on 2023-02-26 17:53

import auctions.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_remove_product_category_product_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='bids',
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ManyToManyField(blank=True, related_name='%(app_label)s_%(class)s_prod_categories', to='auctions.categories'),
        ),
        migrations.AlterField(
            model_name='product',
            name='seller',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_prod_selling', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='ArchiveProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prod_name', models.CharField(max_length=128)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('price_base', models.DecimalField(decimal_places=4, max_digits=19)),
                ('price_cur', models.DecimalField(decimal_places=4, max_digits=19)),
                ('image_path', models.ImageField(upload_to=auctions.models.user_directory_path, verbose_name='Image path')),
                ('description', models.TextField(blank=True)),
                ('date_sold', models.DateTimeField(auto_now_add=True)),
                ('active_product_id', models.BigIntegerField()),
                ('category', models.ManyToManyField(blank=True, related_name='%(app_label)s_%(class)s_prod_categories', to='auctions.categories')),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_prod_selling', to=settings.AUTH_USER_MODEL)),
                ('winner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='win_prod', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
