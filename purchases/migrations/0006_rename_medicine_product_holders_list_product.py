# Generated by Django 4.1.7 on 2023-03-02 12:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('purchases', '0005_rename_product_product_holders_list_medicine'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product_holders_list',
            old_name='medicine',
            new_name='product',
        ),
    ]
