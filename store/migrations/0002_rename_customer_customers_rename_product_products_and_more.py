# Generated by Django 4.2.5 on 2023-09-17 15:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Customer',
            new_name='Customers',
        ),
        migrations.RenameModel(
            old_name='Product',
            new_name='Products',
        ),
        migrations.RenameField(
            model_name='address',
            old_name='customer',
            new_name='Customers',
        ),
        migrations.RenameField(
            model_name='cartitem',
            old_name='product',
            new_name='Products',
        ),
        migrations.RenameField(
            model_name='collections',
            old_name='feature_product',
            new_name='feature_Products',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='customer',
            new_name='Customers',
        ),
        migrations.RenameField(
            model_name='orderitems',
            old_name='product',
            new_name='Products',
        ),
        migrations.RenameIndex(
            model_name='customers',
            new_name='store_Custo_first_n_ec90a0_idx',
            old_name='store_custo_first_n_a7e990_idx',
        ),
        migrations.AlterModelTable(
            name='customers',
            table='store_Customerss',
        ),
    ]