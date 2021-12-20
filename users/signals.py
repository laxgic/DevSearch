from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User

from .models import Profile

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        # print(30*'#' + 'Create Profile' + 30*'#')
        Profile.objects.create(
            user = instance,
            username = instance.username,
            email = instance.email
        )


@receiver(post_delete, sender=Profile)
def delete_user(instance, **kwargs):
    # print(30*'#' + 'Delete Profile' + 30*'#')
    user_obj = instance.user
    user_obj.delete()