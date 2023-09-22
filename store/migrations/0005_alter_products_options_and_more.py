# Generated by Django 4.2.5 on 2023-09-18 20:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_rename_featured_product_id_collections_featured_product'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='products',
            options={'ordering': ['title']},
        ),
        migrations.RenameField(
            model_name='address',
            old_name='Customers',
            new_name='customer',
        ),
        migrations.RenameField(
            model_name='cartitem',
            old_name='Products',
            new_name='product',
        ),
        migrations.RenameField(
            model_name='cartitem',
            old_name='quantitiy',
            new_name='quantity',
        ),
        migrations.RenameField(
            model_name='customers',
            old_name='brith_date',
            new_name='birth_date',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='Customers',
            new_name='customer',
        ),
        migrations.RenameField(
            model_name='orderitems',
            old_name='Products',
            new_name='product',
        ),
        migrations.RenameField(
            model_name='orderitems',
            old_name='quentity',
            new_name='quantity',
        ),
        migrations.RenameIndex(
            model_name='customers',
            new_name='store_Custo_first_n_d3544d_idx',
            old_name='store_Custo_first_n_ec90a0_idx',
        ),
        migrations.AlterField(
            model_name='customers',
            name='membership',
            field=models.CharField(choices=[('MEMBERSHIP_BRONZE', 'Bronze'), ('MEMBERSHIP_SILVER', 'Silver'), ('MEMBERSHIP_GOLD', 'Gold')], default='B', max_length=17),
        ),
        migrations.AlterField(
            model_name='customers',
            name='phone',
            field=models.CharField(max_length=15),
        ),
        migrations.AlterField(
            model_name='order',
            name='payment_status',
            field=models.CharField(choices=[('PAYMENT_STATUS_PENDING', 'Pending'), ('PAYMENT_STATUS_COMPLETE', 'Complete'), ('PAYMENT_STATUS_FAILED', 'Failed')], default='P', max_length=23),
        ),
        migrations.AlterModelTable(
            name='customers',
            table='store_Customers',
        ),
    ]