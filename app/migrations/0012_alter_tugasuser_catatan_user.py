# Generated by Django 4.2.2 on 2023-07-06 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_tugasuser_id_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tugasuser',
            name='catatan_user',
            field=models.TextField(blank=True, null=True),
        ),
    ]
