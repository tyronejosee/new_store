# Generated by Django 4.2.4 on 2023-09-05 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0009_remove_brand_created_at_remove_brand_updated_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='title',
            field=models.CharField(max_length=50, unique=True, verbose_name='Category'),
        ),
    ]
