# Generated by Django 5.1.1 on 2024-09-19 02:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Admin', '0007_tbl_house'),
        ('Guest', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='tbl_owner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('owner_name', models.CharField(max_length=20)),
                ('owner_contact', models.CharField(max_length=20)),
                ('owner_email', models.EmailField(max_length=254)),
                ('owner_gender', models.CharField(max_length=20)),
                ('owner_address', models.TextField()),
                ('owner_photo', models.FileField(upload_to='UserDocs/')),
                ('owner_proof', models.FileField(upload_to='UserDocs/')),
                ('owner_password', models.CharField(max_length=20)),
                ('owner_status', models.IntegerField(default=0)),
                ('house', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Admin.tbl_house')),
            ],
        ),
    ]
