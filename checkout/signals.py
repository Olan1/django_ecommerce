from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import OrderLineItem


# To execute this function whenever the post_save signal is sent, the receiver decorator is told it is recieving post_save signals from the OrderLineItem model
@receiver(post_save, sender=OrderLineItem)
def update_on_save(sender, instance, created, **kwargs):
    """
    Update order total on lineitem update/create
    """
    
    instance.order.update_total()
    
    
# To execute this function whenever the post_delete signal is sent, the receiver decorator is told it is recieving post_delete signals from the OrderLineItem model
@receiver(post_delete, sender=OrderLineItem)
def update_on_delete(sender, instance, **kwargs):
    """
    Update order total on delete of individual lineitem
    """
    
    instance.order.update_total()