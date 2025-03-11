from django.db.models.signals import post_save
from django.dispatch import receiver


from .models import User, OTP

@receiver(post_save, sender=User)
def create_otp(sender, instance, created, **kwargs):
    if created and instance.created_from_app:
        otp = OTP.objects.create(email=instance.email, otp='123456')
        otp.save()
        otp.send_otp_to_user()