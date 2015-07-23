from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from dnsmanager.models import Zone

from .handlers import save_zone, delete_zone


@receiver(post_save, sender=Zone)
def zone_saved(sender, instance, created, **kwargs):
    return save_zone(instance, created)


@receiver(post_delete, sender=Zone)
def zone_deleted(sender, instance, **kwargs):
    return delete_zone(instance)