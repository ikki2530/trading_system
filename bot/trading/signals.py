from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from .models import Profile


def customer_profile(sender, instance, created, **kwargs):
    if created:
        # Agregar a grupo
        group = Group.objects.get(name='users_group')
        print("signal", group, " | instance", instance)
        instance.groups.add(group)
        # Crear profile for user
        Profile.objects.create(
                user=instance,
                name=instance.username,
                email=instance.email
            )

post_save.connect(customer_profile, sender=User)