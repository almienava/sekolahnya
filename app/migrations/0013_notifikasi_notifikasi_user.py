# Generated by Django 4.2.2 on 2023-07-07 09:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_alter_tugasuser_catatan_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notifikasi',
            fields=[
                ('id_notifikasi', models.AutoField(primary_key=True, serialize=False)),
                ('type_notif', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(db_column='created_by', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('id_kelas', models.ForeignKey(db_column='id_kelas', null=True, on_delete=django.db.models.deletion.CASCADE, to='app.kelas')),
            ],
        ),
        migrations.CreateModel(
            name='Notifikasi_user',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status_buka', models.BooleanField(default=False)),
                ('id_notifikasi', models.ForeignKey(db_column='id_notifikasi', on_delete=django.db.models.deletion.CASCADE, to='app.notifikasi')),
                ('id_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
