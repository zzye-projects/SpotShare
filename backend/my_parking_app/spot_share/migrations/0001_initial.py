# Generated by Django 4.2.16 on 2024-10-30 00:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('street', models.CharField(max_length=255)),
                ('street_no', models.SmallIntegerField()),
                ('city', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=100)),
                ('postal_code', models.CharField(max_length=20, unique=True)),
                ('country', models.CharField(max_length=100)),
                ('staff_users', models.ManyToManyField(related_name='addresses', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('make', models.CharField(max_length=50)),
                ('model', models.CharField(max_length=50)),
                ('colour', models.CharField(max_length=30)),
                ('license_plate', models.CharField(db_index=True, max_length=15, unique=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Parking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('parking_unit', models.CharField(max_length=50)),
                ('available_start', models.DateField(db_index=True)),
                ('available_end', models.DateField(blank=True, db_index=True, null=True)),
                ('status', models.CharField(choices=[('DRAFT', 'Draft'), ('ACTIVE', 'Active'), ('ARCHIVED', 'Archived')], db_index=True, default='DRAFT', max_length=10)),
                ('payment_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('payment_frequency', models.CharField(choices=[('ANNUALLY', 'Annually'), ('MONTHLY', 'Monthly'), ('WEEKLY', 'Weekly')], max_length=10)),
                ('payment_type', models.CharField(choices=[('CREDIT', 'Credit'), ('DEBIT', 'Pre-Authorized Debit')], max_length=10)),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='spot_share.address')),
                ('lessor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Lease',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField(db_index=True)),
                ('end_date', models.DateField(blank=True, db_index=True, null=True)),
                ('status', models.CharField(choices=[('DRAFT', 'Draft'), ('ACTIVE', 'Active'), ('ARCHIVED', 'Archived')], default='DRAFT', max_length=10)),
                ('payment_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('payment_frequency', models.CharField(choices=[('ANNUALLY', 'Annually'), ('MONTHLY', 'Monthly'), ('WEEKLY', 'Weekly')], max_length=10)),
                ('payment_type', models.CharField(choices=[('CREDIT', 'Credit'), ('DEBIT', 'Pre-Authorized Debit')], max_length=10)),
                ('payment_details', models.CharField(max_length=255)),
                ('parking', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='spot_share.parking')),
                ('vehicle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='spot_share.vehicle')),
            ],
        ),
    ]
