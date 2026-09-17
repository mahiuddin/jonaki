# stock/signals.py
from django.db import transaction
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from common.constants import (
    MOVEMENT_TYPE_ADJUSTMENT_ADD,
    MOVEMENT_TYPE_DAMAGE,
    MOVEMENT_TYPE_LOST,
)
from .models import StockAdjustment, StockMovement


@receiver(post_save, sender=StockAdjustment)
def handle_stock_adjustment_save(sender, instance, created, **kwargs):
    """Adjusts product stock and logs movement on Damage/Lost record save."""
    with transaction.atomic():
        product = instance.product

        # Stock additions increase balance, Damage/Lost/Sub reduce balance
        if instance.reason == MOVEMENT_TYPE_ADJUSTMENT_ADD:
            ledger_qty = instance.quantity
        else:
            ledger_qty = -instance.quantity  # Negative value for Stock Out

        if created:
            # Update product stock snapshot
            product.quantity += ledger_qty
            product.save(update_fields=['quantity', 'updated_at'])

            # Record Ledger Entry
            StockMovement.objects.create(
                product=product,
                quantity=ledger_qty,
                movement_type=instance.reason,
                reference_number=f"ADJ-{instance.id}",
                remarks=f"Adjustment Reason: {instance.get_reason_display()} | Notes: {instance.remarks or 'N/A'}",
            )
        else:
            # Handle Edits to Adjustments
            movement = StockMovement.objects.filter(
                product=product,
                reference_number=f"ADJ-{instance.id}"
            ).first()

            if movement:
                # Revert old movement from product stock, apply new
                product.quantity -= movement.quantity
                product.quantity += ledger_qty
                product.save(update_fields=['quantity', 'updated_at'])

                # Update existing movement ledger
                movement.quantity = ledger_qty
                movement.movement_type = instance.reason
                movement.remarks = f"Adjustment Reason: {instance.get_reason_display()} | Notes: {instance.remarks or 'N/A'}"
                movement.save(update_fields=['quantity', 'movement_type', 'remarks'])


@receiver(post_delete, sender=StockAdjustment)
def handle_stock_adjustment_delete(sender, instance, **kwargs):
    """Reverts stock balance when an Adjustment record is deleted."""
    with transaction.atomic():
        product = instance.product

        movement = StockMovement.objects.filter(
            product=product,
            reference_number=f"ADJ-{instance.id}"
        ).first()

        if movement:
            # Subtract whatever movement was applied to reverse it
            product.quantity -= movement.quantity
            product.save(update_fields=['quantity', 'updated_at'])
            movement.delete()