# Generated by Django 4.2.5 on 2023-09-25 17:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_alter_orderitems_order'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderitems',
            old_name='Products',
            new_name='products',
        ),
        migrations.RenameField(
            model_name='orderitems',
            old_name='quentity',
            new_name='quantity',
        ),
    ]