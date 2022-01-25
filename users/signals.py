from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings

from .models import Profile

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        # print(30*'#' + 'Create Profile' + 30*'#')
        profile = Profile.objects.create(
            user = instance,
            name = instance.first_name,
            username = instance.username,
            email = instance.email
        )

        subject = 'Welcome to this Website!'
        message = 'We are glad you are here.'
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [profile.email],
            fail_silently=False,
        )


@receiver(post_delete, sender=Profile)
def delete_user(instance, **kwargs):
    # print(30*'#' + 'Delete Profile' + 30*'#')
    user_obj = instance.user
    user_obj.delete()



@receiver(post_save, sender=Profile)
def update_user(instance, created, **kwargs):
    profile = instance
    user = profile.user
    if created == False:
        user.first_name = profile.name
        user.username = profile.username
        user.email = profile.email
        user.save()