# Generated by Django 5.1.1 on 2024-09-19 03:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Guest', '0002_tbl_owner'),
    ]

    operations = [
        migrations.DeleteModel(
            name='tbl_owner',
        ),
    ]
