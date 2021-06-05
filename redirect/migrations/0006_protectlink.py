# Generated by Django 3.1.8 on 2021-05-12 16:29

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('redirect', '0005_redirectlink_url2'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProtectLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.CharField(max_length=10485700)),
                ('password', models.UUIDField(default=uuid.UUID('9c055c66-c8b4-468a-910a-18f97e1fef80'), editable=False)),
            ],
        ),
    ]