from decimal import Decimal

from django.db import transaction
from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver

from common.constants import MOVEMENT_TYPE_PURCHASE, MOVEMENT_TYPE_RETURN_SUPPLIER
from stocks.models import StockMovement
from suppliers.models import Supplier
from .models import  Purchase, PurchaseItem, PurchaseReturn, PurchaseReturnItem

@receiver(pre_save, sender=Purchase)
def purchase_pre_save(sender, instance, **kwargs):

    if instance.pk:
        try:
            old_purchase = Purchase.objects.get(pk=instance.pk)

            instance._old_net_amount = old_purchase.net_amount
            instance._old_supplier_id = old_purchase.supplier_id

        except Purchase.DoesNotExist:
            instance._old_net_amount = Decimal('0.00')
            instance._old_supplier_id = None

    else:
        instance._old_net_amount = Decimal('0.00')
        instance._old_supplier_id = None

@receiver(post_save, sender=Purchase)
def purchase_post_save(sender, instance, created, **kwargs):

    old_amount = getattr(
        instance,
        '_old_net_amount',
        Decimal('0.00')
    )

    old_supplier_id = getattr(
        instance,
        '_old_supplier_id',
        None
    )

    new_amount = instance.net_amount or Decimal('0.00')

    # New Purchase
    if created:

        supplier = instance.supplier

        supplier.due_amount += new_amount

        supplier.save(
            update_fields=['due_amount', 'updated_at']
        )

        return

    # Supplier changed
    if old_supplier_id != instance.supplier_id:

        if old_supplier_id:

            old_supplier = Supplier.objects.get(
                pk=old_supplier_id
            )

            old_supplier.due_amount -= old_amount

            old_supplier.save(
                update_fields=['due_amount', 'updated_at']
            )

        new_supplier = instance.supplier

        new_supplier.due_amount += new_amount

        new_supplier.save(
            update_fields=['due_amount', 'updated_at']
        )

        return

    # Same supplier, but net amount changed
    difference = new_amount - old_amount

    if difference != 0:

        supplier = instance.supplier

        supplier.due_amount += difference

        supplier.save(
            update_fields=['due_amount', 'updated_at']
        )

@receiver(post_delete, sender=Purchase)
def handle_purchase_delete(sender, instance, **kwargs):

    supplier = instance.supplier

    supplier.due_amount -= instance.net_amount

    supplier.save(
        update_fields=['due_amount', 'updated_at']
    )

@receiver(post_save, sender=PurchaseItem)
def handle_purchase_item_save(sender, instance, created, **kwargs):
    """Handles stock increments on creation AND adjustments on updates."""
    with transaction.atomic():
        product = instance.product
        purchase = instance.purchase
        if created:
            # --- 1. NEW PURCHASE ITEM ---
            product.quantity += instance.quantity
            if instance.purchase_price > 0:
                product.buying_price = instance.purchase_price
            product.save(
                update_fields=['quantity', 'buying_price', 'updated_at']
            )

            # Create initial stock movement ledger entry
            StockMovement.objects.create(
                product=product,
                quantity=instance.quantity,
                movement_type=MOVEMENT_TYPE_PURCHASE,
                reference_number=instance.purchase.purchase_number,
                remarks=f"PurchaseItem ID: {instance.id} | Supplier: {instance.purchase.supplier.name}",
            )

        else:
            # --- 2. UPDATED PURCHASE ITEM ---
            # Locate the exact movement linked to this specific PurchaseItem ID
            movement = StockMovement.objects.filter(
                product=product,
                movement_type=MOVEMENT_TYPE_PURCHASE,
                reference_number=instance.purchase.purchase_number,
                remarks__contains=f"PurchaseItem ID: {instance.id}",
            ).first()

            if movement:
                # Calculate net difference (New Quantity - Old Quantity)
                # Example: Was 10, updated to 15 -> difference is +5
                # Example: Was 10, updated to 7  -> difference is -3
                qty_difference = instance.quantity - movement.quantity

                if qty_difference != 0:
                    # Adjust cached product balance by net difference
                    product.quantity += qty_difference
                    if instance.purchase_price > 0:
                        product.buying_price = instance.purchase_price
                    product.save(
                        update_fields=['quantity', 'buying_price', 'updated_at']
                    )

                    # Update movement record to match new quantity
                    movement.quantity = instance.quantity
                    movement.save(update_fields=['quantity'])


@receiver(post_delete, sender=PurchaseItem)
def handle_purchase_item_delete(sender, instance, **kwargs):
    """Reverts product stock and deletes the movement if a PurchaseItem line is deleted."""
    with transaction.atomic():
        product = instance.product
        purchase = instance.purchase

        # Deduct deleted purchase quantity from product stock balance
        product.quantity -= instance.quantity
        product.save(update_fields=['quantity', 'updated_at'])

        # Delete corresponding movement ledger record
        StockMovement.objects.filter(
            product=product,
            movement_type=MOVEMENT_TYPE_PURCHASE,
            reference_number=instance.purchase.purchase_number,
            remarks__contains=f"PurchaseItem ID: {instance.id}",
        ).delete()

@receiver(post_save, sender=PurchaseReturnItem)
def handle_purchase_return_item_save(sender, instance, created, **kwargs):
    """Deducts stock on item save and records ledger movement."""
    with transaction.atomic():
        product = instance.product
        parent_return = instance.purchase_return

        # supplier = instance.purchase_return.supplier

        if created:
            # 1. NEW ITEM: Deduct stock balance (Stock Out)
            product.quantity -= instance.quantity
            product.save(update_fields=['quantity', 'updated_at'])

            # Returning goods reduces what we owe
            # supplier.due_amount -= instance.total_amount
            # supplier.save(update_fields=['due_amount', 'updated_at'])

            # Log negative movement entry in Stock Ledger
            StockMovement.objects.create(
                product=product,
                quantity=-instance.quantity,
                movement_type=MOVEMENT_TYPE_RETURN_SUPPLIER,
                reference_number=parent_return.return_number,
                movement_date=parent_return.return_date,
                remarks=f'Supplier Return ID: {parent_return.id} | Supplier: {parent_return.supplier.name}',
            )

        else:
            # 2. UPDATED ITEM: Reconcile difference
            movement = StockMovement.objects.filter(
                product=product,
                movement_type=MOVEMENT_TYPE_RETURN_SUPPLIER,
                reference_number=parent_return.return_number,
            ).first()

            if movement:
                old_qty = abs(movement.quantity)
                qty_difference = instance.quantity - old_qty

                if qty_difference != 0:
                    product.quantity -= qty_difference
                    product.save(update_fields=['quantity', 'updated_at'])

                    movement.quantity = -instance.quantity
                    movement.movement_date = parent_return.return_date
                    movement.save(update_fields=['quantity', 'movement_date'])


@receiver(post_delete, sender=PurchaseReturnItem)
def handle_purchase_return_item_delete(sender, instance, **kwargs):
    """Reverts product stock if a return line item is deleted."""
    with transaction.atomic():
        product = instance.product
        parent_return = instance.purchase_return

        # Deleting a return restores what we owe
        # parent_return.supplier.due_amount += parent_return.total_amount
        # parent_return.supplier.save(update_fields=['due_amount', 'updated_at'])

        # Restore returned stock back into inventory balance
        product.quantity += instance.quantity
        product.save(update_fields=['quantity', 'updated_at'])

        # Remove corresponding ledger entry
        StockMovement.objects.filter(
            product=product,
            movement_type=MOVEMENT_TYPE_RETURN_SUPPLIER,
            reference_number=parent_return.return_number,
        ).delete()
