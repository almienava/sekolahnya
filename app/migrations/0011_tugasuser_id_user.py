# Generated by Django 4.2.2 on 2023-07-06 02:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_tugas_alter_userdata_profile_pic_tugasuser'),
    ]

    operations = [
        migrations.AddField(
            model_name='tugasuser',
            name='id_user',
            field=models.ForeignKey(db_column='id_user', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
