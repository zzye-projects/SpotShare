# Generated by Django 4.2.16 on 2024-10-24 19:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spot_share', '0002_address_users'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='postal_code',
            field=models.CharField(max_length=20, unique=True),
        ),
    ]
