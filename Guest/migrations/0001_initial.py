# Generated by Django 5.1.1 on 2024-09-16 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='tbl_user',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=20)),
                ('user_contact', models.CharField(max_length=20)),
                ('user_email', models.EmailField(max_length=254)),
                ('user_gender', models.CharField(max_length=20)),
                ('user_address', models.TextField()),
                ('user_photo', models.FileField(upload_to='UserDocs/')),
                ('user_proof', models.FileField(upload_to='UserDocs/')),
                ('user_password', models.CharField(max_length=20)),
                ('user_status', models.IntegerField(default=0)),
            ],
        ),
    ]
