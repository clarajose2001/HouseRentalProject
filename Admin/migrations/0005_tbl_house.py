# Generated by Django 5.1.1 on 2024-09-17 02:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Admin', '0004_delete_tbl_house'),
    ]

    operations = [
        migrations.CreateModel(
            name='tbl_house',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('house_title', models.CharField(max_length=10)),
                ('house_description', models.CharField(max_length=100)),
                ('house_price', models.IntegerField()),
                ('house_image', models.FileField(upload_to='HouseDocs/')),
                ('house_location', models.CharField(max_length=50)),
                ('house_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Admin.tbl_category')),
            ],
        ),
    ]
