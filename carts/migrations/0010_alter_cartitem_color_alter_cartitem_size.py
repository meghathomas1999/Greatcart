# Generated by Django 4.2.4 on 2023-08-21 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0009_alter_cart_id_alter_cartitem_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='color',
            field=models.CharField(default='seleced_color', max_length=50),
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='size',
            field=models.CharField(default='seleced_size', max_length=50),
        ),
    ]