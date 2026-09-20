# suppliers/resources.py
from import_export import fields, resources
from .models import Supplier


class SupplierDueUpdateResource(resources.ModelResource):
    id = fields.Field(attribute='id', column_name='Supplier ID')
    name = fields.Field(attribute='name', column_name='Supplier Name')
    contact_number = fields.Field(
        attribute='contact_number', column_name='Contact'
    )
    due_amount = fields.Field(attribute='due_amount', column_name='Due Amount')

    class Meta:
        model = Supplier
        # Use ID to identify existing records during re-import
        import_id_fields = ['id']
        fields = ('id', 'name', 'contact_number', 'due_amount')
        export_order = ('id', 'name', 'contact_number', 'due_amount')
        skip_unchanged = True
        report_skipped = True