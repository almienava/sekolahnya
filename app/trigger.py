from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import *



@receiver(post_save, sender=Notifikasi)
def insert_notif_to_all(sender, instance, created, **kwargs):
    if created:
        user_data = UserData.objects.filter(id_kelas=instance.id_kelas)
        notifikasi_user_objects = []
        
        for user in user_data:
            notifikasi_user_objects.append(Notifikasi_user(id_notifikasi=instance, 
                                                           id_user=user,
                                                             status_buka=False))
        Notifikasi_user.objects.bulk_create(notifikasi_user_objects)



@receiver(post_save,sender=BoardingKelas)
def notif_boarding(sender,instance,created,**kwargs):
    if created:
        idKelas =""
        if instance.id_kelas is not None:
            idKelas = instance.id_kelas
        Notifikasi.objects.create(created_by=instance.pengirim,
                                   type_notif="boarding", 
                                   id_kelas=idKelas)

@receiver(post_save,sender=HistoriTransaksiKas)
def notif_historiTransaksi(sender,instance,created,**kwargs):
    if created:
        jenis = "Pembayaran Kas"
        if instance.jenis == 0:
            jenis = "Salah Input Kas"
        Notifikasi.objects.create(created_by=instance.id_user,
                                  type_notif=jenis,
                                  id_kelas=instance.id_kelas)