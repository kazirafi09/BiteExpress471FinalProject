# Generated by Django 5.0.6 on 2024-07-27 07:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('members', '0008_remove_fooditem_remaining_stock'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('total_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('status', models.CharField(choices=[('PENDING', 'Pending'), ('CONFIRMED', 'Confirmed'), ('IN_PROGRESS', 'In Progress'), ('DELIVERED', 'Delivered'), ('CANCELLED', 'Cancelled')], default='PENDING', max_length=20)),
                ('buyer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='members.buyer')),
                ('food_items', models.ManyToManyField(to='members.fooditem')),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='members.restaurant')),
            ],
        ),
    ]
