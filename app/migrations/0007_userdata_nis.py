# Generated by Django 4.2.2 on 2023-07-05 01:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_pelajaran_jadwalpelajaran'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdata',
            name='nis',
            field=models.BigIntegerField(max_length=50, null=True),
        ),
    ]
