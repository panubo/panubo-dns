from django.db.models.signals import post_delete
from django.dispatch import receiver

from dnsmanager.models import Zone
from dnsmanager.signals import zone_fully_saved_signal

from .handlers import save_zone, delete_zone


@receiver(zone_fully_saved_signal)
def zone_saved(sender, instance, created, **kwargs):
    return save_zone(instance, created)


@receiver(post_delete, sender=Zone)
def zone_deleted(sender, instance, **kwargs):
    return delete_zone(instance)