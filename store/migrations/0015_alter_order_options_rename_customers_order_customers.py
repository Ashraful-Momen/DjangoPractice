# Generated by Django 4.2.5 on 2023-09-24 18:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0014_rename_brith_date_customers_birth_date_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'permissions': [('cancel_order', 'Can cancel Order')]},
        ),
        migrations.RenameField(
            model_name='order',
            old_name='Customers',
            new_name='customers',
        ),
    ]