# Generated by Django 4.2.3 on 2023-08-03 05:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trendico', '0002_product_created_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='label',
        ),
    ]
