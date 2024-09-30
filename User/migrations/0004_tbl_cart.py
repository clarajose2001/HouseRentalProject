# Generated by Django 5.1.1 on 2024-09-17 02:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Admin', '0005_tbl_house'),
        ('User', '0003_delete_tbl_cart'),
    ]

    operations = [
        migrations.CreateModel(
            name='tbl_cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cart_qty', models.IntegerField()),
                ('cart_status', models.CharField(default=0, max_length=10)),
                ('house', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Admin.tbl_house')),
            ],
        ),
    ]
