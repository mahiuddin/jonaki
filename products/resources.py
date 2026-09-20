# products/resources.py
from import_export import fields, resources
from .models import Product


class ProductBulkUpdateResource(resources.ModelResource):
    sku = fields.Field(attribute='sku', column_name='SKU')
    name = fields.Field(attribute='name', column_name='Product Name')
    measurement_type = fields.Field(attribute='measurement_type', column_name='Measurement Type')

    # --- READ-ONLY NAME FIELDS FOR CONTEXT ON EXPORT ---
    category_name = fields.Field(
        attribute='category__name',
        column_name='category_name',
        readonly=True,
    )
    product_type_name = fields.Field(
        attribute='product_type__name',
        column_name='product_type_name',
        readonly=True,
    )
    brand_name = fields.Field(
        attribute='brand__name', column_name='brand_name', readonly=True
    )

    # --- EXACT DATABASE FOREIGN KEY ID FIELDS FOR IMPORT & UPDATE ---
    category_id = fields.Field(attribute='category_id', column_name='category_id')
    product_type_id = fields.Field(
        attribute='product_type_id', column_name='product_type_id'
    )
    brand_id = fields.Field(attribute='brand_id', column_name='brand_id')

    size = fields.Field(attribute='size', column_name='size')
    quantity = fields.Field(attribute='quantity', column_name='quantity')
    buying_price = fields.Field(attribute='buying_price', column_name='buying_price')

    class Meta:
        model = Product
        import_id_fields = ['sku']  # Identifies existing records by SKU
        fields = (
            'sku',
            'name',
            'measurement_type',
            'category_name',
            'category_id',
            'product_type_name',
            'product_type_id',
            'brand_name',
            'brand_id',
            'size',
            'quantity',
            'buying_price',
        )
        export_order = (
            'sku',
            'name',
            'measurement_type',
            'category_name',
            'category_id',
            'product_type_name',
            'product_type_id',
            'brand_name',
            'brand_id',
            'size',
            'quantity',
            'buying_price',
        )
        skip_unchanged = True
        report_skipped = True