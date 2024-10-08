# Generated by Django 5.1.1 on 2024-09-22 02:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Admin', '0007_tbl_house'),
        ('Guest', '0007_delete_tbl_owner'),
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
                ('houses', models.ManyToManyField(blank=True, to='Admin.tbl_house')),
            ],
        ),
    ]
