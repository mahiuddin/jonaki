# products/resources.py
from import_export import fields, resources
from .models import Product, ProductType


class ProductBulkUpdateResource(resources.ModelResource):
    id = fields.Field(attribute='id', column_name='Product ID')
    sku = fields.Field(attribute='sku', column_name='SKU')
    name = fields.Field(attribute='name', column_name='Product Name')
    category = fields.Field(
        attribute='category__name', column_name='Category'
    )
    product_type = fields.Field(
        attribute='product_type__name', column_name='Product Type'
    )
    size = fields.Field(attribute='size', column_name='Size')
    quantity = fields.Field(attribute='quantity', column_name='Stock Quantity')
    buying_price = fields.Field(
        attribute='buying_price', column_name='Buying Price'
    )

    class Meta:
        model = Product
        # ID is crucial for matching existing records during import
        import_id_fields = ['id']
        fields = ('id', 'sku', 'name', 'category', 'product_type', 'size', 'quantity', 'buying_price')
        export_order = (
            'id',
            'sku',
            'name',
            'category',
            'product_type',
            'size',
            'quantity',
            'buying_price',
        )
        skip_unchanged = True
        report_skipped = True