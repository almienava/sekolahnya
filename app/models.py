from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.conf import settings
import uuid
from datetime import datetime
from django.shortcuts import get_object_or_404
from django.db.models.signals import post_save
from django.dispatch import receiver


class CustomUserManager(BaseUserManager):
    def create_user(self, nama_lengkap, username, email, no_hp, password=None, is_login=False, role=None, approved=False,profile_pic=None,id_parent_user=None,id_kelas=None):
        if not email:
            raise ValueError('Email harus diisi')

        email = self.normalize_email(email)
        user = self.model(nama_lengkap=nama_lengkap, username=username, email=email, no_hp=no_hp, is_login=is_login, role=role, approved=approved,profile_pic=profile_pic,id_parent_user=id_parent_user,id_kelas=id_kelas)
        user.set_password(password)
        user.save(using=self._db)
        return user

class UserData(AbstractBaseUser):
    id_user = models.CharField(primary_key=True, default=uuid.uuid4, editable=False)
    nis = models.BigIntegerField(null=True)
    nama_lengkap = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    id_kelas = models.ForeignKey('Kelas', on_delete=models.CASCADE,null=True, db_column='id_kelas')
    no_hp = models.BigIntegerField()
    password = models.CharField(max_length=255)
    is_login = models.BooleanField(default=False)
    create_dtm = models.DateTimeField(auto_now_add=True)
    id_parent_user = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, related_name='parent_users',db_column='id_parent_user')
    profile_pic = models.TextField(null=True, blank=True)
    username = models.CharField(max_length=255, unique=True)
    role = models.CharField(max_length=255)
    approved = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    objects = CustomUserManager()

    def __str__(self):
        return self.username

class Kelas(models.Model):
    id_kelas = models.AutoField(primary_key=True)
    nama_kelas = models.CharField(max_length=255)
    id_user = models.ForeignKey(UserData, on_delete=models.CASCADE, db_column='id_guru')
    jurusan = models.CharField(max_length=255, null=True)

class JadwalPiket(models.Model):
    id_piket = models.AutoField(primary_key=True)
    hari = models.CharField(max_length=10,null=True)
    id_user = models.ForeignKey(UserData, on_delete=models.CASCADE,null=True,db_column='id_user')
    id_kelas = models.ForeignKey(Kelas, on_delete=models.CASCADE,null=True,db_column='id_kelas')


# 0 = salah input kas
# 1 = Pemasukan Kas
# 2 = Pemasukan Lain
# 3 = Pengeluaran kas
class Kas(models.Model):
    id_trx_kas = models.AutoField(primary_key=True)
    id_user = models.ForeignKey(UserData, on_delete=models.CASCADE,null=True,db_column='id_user')
    id_kelas = models.ForeignKey(Kelas, on_delete=models.CASCADE,null=True,db_column='id_kelas')
    nominal = models.BigIntegerField(null=True, db_column='nominal')
    w1 = models.BooleanField(default=False)
    w1_dtm = models.DateTimeField()
    w2 = models.BooleanField(default=False)
    w2_dtm = models.DateTimeField()
    w3 = models.BooleanField(default=False)
    w3_dtm = models.DateTimeField()
    w4 = models.BooleanField(default=False)
    w4_dtm = models.DateTimeField()
    w5 = models.BooleanField(default=False)
    w5_dtm = models.DateTimeField()
    yearmonth = models.BigIntegerField(null=True)

class HistoriTransaksiKas(models.Model):
    id_historiKas = models.AutoField(primary_key=True)
    id_user = models.ForeignKey(UserData, on_delete=models.CASCADE,null=True,db_column='id_user')
    id_kelas = models.ForeignKey(Kelas, on_delete=models.CASCADE,null=True,db_column='id_kelas')
    deskripsi = models.TextField(null=True)
    jenis = models.SmallIntegerField(default=1)
    nominal = models.BigIntegerField(null=True,db_column='nominal')
    tanggal_histori = models.DateTimeField(auto_now_add=True)

    @classmethod
    def create_histori(cls,id_user,id_kelas,deskripsi,jenis,nominal):
        user = get_object_or_404(UserData,id_user=id_user)
        kelas = get_object_or_404(Kelas,id_kelas=id_kelas)

        histori = cls(id_user=user,id_kelas=kelas,deskripsi=deskripsi,jenis=jenis,nominal=nominal)
        histori.save()
        return True
        

class Pelajaran(models.Model):
    id_pelajaran = models.AutoField(primary_key=True)
    nama_pelajaran = models.CharField(max_length=150)
    id_guru = models.ForeignKey(UserData,on_delete=models.CASCADE,null=True,db_column='id_guru')
    created_at= models.DateTimeField(auto_now_add=True)

class JadwalPelajaran(models.Model):
    id_jadwalpelajaran = models.AutoField(primary_key=True)
    hari = models.CharField(max_length=10,null=True)
    jam_pelajaran = models.CharField(max_length=10,null=True)
    id_pelajaran = models.ForeignKey(Pelajaran, on_delete=models.CASCADE,null=True,db_column='id_pelajaran') 
    id_kelas = models.ForeignKey(Kelas, on_delete=models.CASCADE,null=True,db_column='id_kelas')

class Tugas(models.Model):
    id_tugas = models.CharField(primary_key=True, default=uuid.uuid4, editable=False,db_column='id_tugas')
    id_pelajaran = models.ForeignKey(Pelajaran, on_delete=models.CASCADE,null=True,db_column='id_pelajaran') 
    id_kelas = models.ForeignKey(Kelas, on_delete=models.CASCADE,null=True,db_column='id_kelas')
    nama_tugas = models.CharField(max_length=255,null=True)
    deskripsi = models.TextField(null=True)
    path_file = models.TextField(null=True)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    created_tugas =models.DateTimeField(auto_now_add=True)

class TugasUser(models.Model):
    id_tugas = models.ForeignKey(Tugas,on_delete=models.CASCADE,db_column='id_tugas')
    catatan_user = models.TextField(null=True,blank=True)
    status_tugas = models.SmallIntegerField(default =0)
    path_tugas = models.TextField(null=True)
    update_at = models.DateTimeField(auto_now_add=True)
    id_user = models.ForeignKey(UserData,on_delete=models.CASCADE,db_column='id_user',null=True)

class Notifikasi(models.Model):
    id_notifikasi = models.AutoField(primary_key=True)
    type_notif = models.CharField(max_length=255)
    created_by = models.ForeignKey(UserData,on_delete=models.CASCADE,db_column='created_by')
    created_at = models.DateTimeField(auto_now_add=True)
    id_kelas = models.ForeignKey(Kelas,on_delete=models.CASCADE,null=True,db_column='id_kelas')

class Notifikasi_user(models.Model):
    id_notifikasi = models.ForeignKey(Notifikasi,on_delete=models.CASCADE,db_column='id_notifikasi')
    id_user = models.ForeignKey(UserData,on_delete=models.CASCADE,db_column='id_user')
    status_buka = models.BooleanField(default=False)


class BoardingKelas(models.Model):
    id_boarding = models.AutoField(primary_key=True)
    pesan = models.TextField(null=True)
    path_file = models.TextField(null=True)
    pengirim = models.ForeignKey(UserData,on_delete=models.CASCADE,db_column='pengirim')
    id_kelas = models.ForeignKey(Kelas,on_delete=models.CASCADE,null=True,db_column='id_kelas')
    created_at = models.DateTimeField(auto_now_add=True)

    @classmethod
    def create_boarding(cls, pesan, pengirim_id, id_kelas_id):
        pengirim = get_object_or_404(UserData, id_user=pengirim_id)
        id_kelas = get_object_or_404(Kelas, id_kelas=id_kelas_id)
        
        boarding = cls.objects.create(pesan=pesan, pengirim=pengirim, id_kelas=id_kelas)
        boarding.save()       
        return True
