# Generated by Django 4.2.16 on 2024-10-30 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spot_share', '0004_lease_lessor_lease_lessor_approved_lease_tenant_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lease',
            name='lessor_approved',
            field=models.CharField(choices=[('PENDING', 'Pending'), ('APPROVED', 'Approved'), ('REJECTED', 'Rejected')], default='PENDING', max_length=10),
        ),
        migrations.AlterField(
            model_name='lease',
            name='tenant_approved',
            field=models.CharField(choices=[('PENDING', 'Pending'), ('APPROVED', 'Approved'), ('REJECTED', 'Rejected')], default='PENDING', max_length=10),
        ),
    ]
