from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.conf import settings
import uuid



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
    status_tugas = models.IntegerField(default =0)
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
    id_user = models.ForeignKey(UserData,on_delete=models.CASCADE)
    status_buka = models.BooleanField(default=False)


# class DepositMethod(models.Model):
#     method_id = models.AutoField(primary_key=True)
#     name = models.SlugField(max_length=100, unique=True)
#     address_wallet = models.CharField(max_length=150)

# class Deposit(models.Model):
#     id_trx = models.CharField(default=uuid.uuid4, editable=False, unique=True)
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#     method = models.ForeignKey(DepositMethod, on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)
#     status_approve = models.IntegerField(default=0)
#     expired_at = models.DateTimeField()


# class Withdraw(models.Model):
#     id_withdraw =models.CharField(default=uuid.uuid4,editable=False,unique=True)
#     user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#     method = models.ForeignKey(DepositMethod, on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)
#     status_withdraw = models.IntegerField(default=0)
#     address = models.CharField(max_length=150)


# class CustomUserManager(BaseUserManager):
#     def create_user(self, nama_lengkap, username, email, no_hp, password=None, is_login=False, role=None, referral_code=None):
#         if not email:
#             raise ValueError('Email harus diisi')

#         email = self.normalize_email(email)
#         user = self.model(nama_lengkap=nama_lengkap, username=username, email=email, no_hp=no_hp, is_login=is_login, role=role, referral_code=username)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

# class CustomUser(AbstractBaseUser):
#     id_user = models.CharField(primary_key=True, default=uuid.uuid4, editable=False)
#     nama_lengkap = models.CharField(max_length=255)
#     username = models.CharField(max_length=150, unique=True)
#     email = models.EmailField(unique=True)
#     no_hp = models.CharField(max_length=15)
#     password = models.CharField(max_length=128)
#     is_login = models.BooleanField(default=False)
#     create_dtm = models.DateTimeField(auto_now_add=True)
#     role = models.CharField(max_length=50, null=True, blank=True)
#     referral_code = models.CharField(max_length=50, null=True, blank=True)
#     balance = models.IntegerField(default=5)
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['username']
#     objects = CustomUserManager()

#     def __str__(self):
#         return self.username



