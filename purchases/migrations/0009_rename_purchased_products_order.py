# Generated by Django 4.1.7 on 2023-03-07 12:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('purchases', '0008_rename_order_purchased_products_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Purchased_Products',
            new_name='Order',
        ),
    ]
