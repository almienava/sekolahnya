# Generated by Django 4.2.2 on 2023-07-06 02:14

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_alter_userdata_profile_pic'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tugas',
            fields=[
                ('id_tugas', models.CharField(db_column='id_tugas', default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('nama_tugas', models.CharField(max_length=255, null=True)),
                ('deskripsi', models.TextField(null=True)),
                ('path_file', models.TextField(null=True)),
                ('start_date', models.DateField(null=True)),
                ('end_date', models.DateField(null=True)),
                ('created_tugas', models.DateTimeField(auto_now_add=True)),
                ('id_kelas', models.ForeignKey(db_column='id_kelas', null=True, on_delete=django.db.models.deletion.CASCADE, to='app.kelas')),
                ('id_pelajaran', models.ForeignKey(db_column='id_pelajaran', null=True, on_delete=django.db.models.deletion.CASCADE, to='app.pelajaran')),
            ],
        ),
        migrations.AlterField(
            model_name='userdata',
            name='profile_pic',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name='TugasUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('catatan_user', models.TextField(null=True)),
                ('status_tugas', models.IntegerField(default=0)),
                ('path_tugas', models.TextField(null=True)),
                ('update_at', models.DateTimeField(auto_now_add=True)),
                ('id_tugas', models.ForeignKey(db_column='id_tugas', on_delete=django.db.models.deletion.CASCADE, to='app.tugas')),
            ],
        ),
    ]