# Generated by Django 4.2.4 on 2023-08-23 11:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0007_remove_orderproduct_variation_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderproduct',
            old_name='poduct_price',
            new_name='product_price',
        ),
    ]
