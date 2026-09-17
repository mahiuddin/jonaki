from django.db import transaction
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from common.constants import MOVEMENT_TYPE_RETURN_CUSTOMER, MOVEMENT_TYPE_SALE
from stocks.models import StockMovement
from .models import OrderItem, OrderReturn


@receiver(post_save, sender=OrderItem)
def handle_sale_item_save(sender, instance, created, **kwargs):
    """Reduces Product stock balance on sale creation and adjusts on edits."""
    with transaction.atomic():
        product = instance.product

        if created:
            # --- 1. NEW SALE ITEM ---
            # Sales reduce stock, so we subtract the sold quantity
            product.quantity -= instance.quantity
            product.save(update_fields=['quantity', 'updated_at'])

            # Record stock-out movement ledger entry (Stored as negative quantity for OUT)
            StockMovement.objects.create(
                product=product,
                quantity=-instance.quantity,  # Negative for Stock Out
                movement_type=MOVEMENT_TYPE_SALE,
                reference_number=instance.order.memo_number,  # Or instance.order.memo_number if that's the unique identifier
                remarks=f"OrderItem ID: {instance.id} | Customer: {instance.order.customer.name}",
            )

        else:
            # --- 2. UPDATED SALE ITEM ---
            movement = StockMovement.objects.filter(
                product=product,
                movement_type=MOVEMENT_TYPE_SALE,
                reference_number=instance.order.memo_number,
                remarks__contains=f"OrderItem ID: {instance.id}",
            ).first()

            if movement:
                # Absolute stored movement quantity
                old_qty = abs(movement.quantity)
                # Calculate quantity difference
                # Example: Sold 5, updated to 8 -> Net diff is +3 additional items sold
                qty_difference = instance.quantity - old_qty

                if qty_difference != 0:
                    # Deduct the difference from product balance
                    product.quantity -= qty_difference
                    product.save(update_fields=['quantity', 'updated_at'])

                    # Update movement record (Keep negative sign for Stock Out)
                    movement.quantity = -instance.quantity
                    movement.save(update_fields=['quantity'])


@receiver(post_delete, sender=OrderItem)
def handle_order_item_delete(sender, instance, **kwargs):
    """Reverts product stock if an OrderItem line is deleted."""
    with transaction.atomic():
        product = instance.product

        # Add sold items back into inventory balance
        product.quantity += instance.quantity
        product.save(update_fields=['quantity', 'updated_at'])

        # Delete corresponding stock-out ledger record
        StockMovement.objects.filter(
            product=product,
            movement_type=MOVEMENT_TYPE_SALE,
            reference_number=instance.order.memo_number,
            remarks__contains=f"OrderItem ID: {instance.id}",
        ).delete()


@receiver(post_save, sender=OrderReturn)
def handle_order_return_save(sender, instance, created, **kwargs):
    """Increases Product stock balance on Sales Return and logs Stock Movement."""
    with transaction.atomic():
        product = instance.product

        if created:
            # --- 1. NEW SALES RETURN ---
            # Customer returns product -> Stock Increases (+)
            product.quantity += instance.quantity
            product.save(update_fields=['quantity', 'updated_at'])

            # Record Ledger Entry (Positive quantity for Stock In)
            StockMovement.objects.create(
                product=product,
                quantity=instance.quantity,  # Positive for Customer Return
                movement_type=MOVEMENT_TYPE_RETURN_CUSTOMER,
                reference_number=f'RET-{instance.order.memo_number}',
                movement_date=instance.return_date,
                remarks=f'Order Return ID: {instance.id} | Reason: {instance.remarks or "N/A"}',
            )

        else:
            # --- 2. UPDATED SALES RETURN ---
            movement = StockMovement.objects.filter(
                product=product,
                movement_type=MOVEMENT_TYPE_RETURN_CUSTOMER,
                reference_number=f'RET-{instance.order.memo_number}',
                remarks__contains=f'Order Return ID: {instance.id}',
            ).first()

            if movement:
                # Difference: New Qty - Old Qty
                qty_difference = instance.quantity - movement.quantity

                if qty_difference != 0:
                    product.quantity += qty_difference
                    product.save(update_fields=['quantity', 'updated_at'])

                    movement.quantity = instance.quantity
                    movement.movement_date = instance.return_date
                    movement.save(update_fields=['quantity', 'movement_date'])


@receiver(post_delete, sender=OrderReturn)
def handle_order_return_delete(sender, instance, **kwargs):
    """Reverts product stock if a Sales Return entry is deleted."""
    with transaction.atomic():
        product = instance.product

        # Deduct the returned stock back from product inventory balance
        product.quantity -= instance.quantity
        product.save(update_fields=['quantity', 'updated_at'])

        # Delete corresponding ledger record
        StockMovement.objects.filter(
            product=product,
            movement_type=MOVEMENT_TYPE_RETURN_CUSTOMER,
            reference_number=f'RET-{instance.order.memo_number}',
            remarks__contains=f'Order Return ID: {instance.id}',
        ).delete()