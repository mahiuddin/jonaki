# suppliers/signals.py
from django.db import transaction
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from .models import SupplierPayment


@receiver(post_save, sender=SupplierPayment)
def handle_supplier_payment_due(sender, instance, created, **kwargs):
    with transaction.atomic():
        supplier = instance.supplier

        if created:
            # Cash paid reduces what we owe
            supplier.due_amount -= instance.amount
            supplier.save(update_fields=['due_amount', 'updated_at'])


@receiver(post_delete, sender=SupplierPayment)
def handle_supplier_payment_due_delete(sender, instance, **kwargs):
    with transaction.atomic():
        supplier = instance.supplier

        # Deleting payment restores what we owe
        supplier.due_amount += instance.amount
        supplier.save(update_fields=['due_amount', 'updated_at'])