# Generated by Django 3.2 on 2021-04-29 10:04

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('redirect', '0002_auto_20210422_2101'),
    ]

    operations = [
        migrations.CreateModel(
            name='RedirectLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.CharField(max_length=10485700)),
                ('unique_id', models.UUIDField(
                    default=uuid.uuid4, editable=False, unique=True)),
                ('url', models.CharField(max_length=10485700, null=True)),
            ],
        ),
    ]
