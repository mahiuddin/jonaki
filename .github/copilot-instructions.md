# Jonaki Machinery Store - AI Coding Agent Instructions

## Project Overview
This is a Django 5.2 machinery store management system (Bangladesh-based business) with multi-app architecture. The application manages inventory, sales, employees, finances, and customer relationships.

**Stack**: Django 5.2, PostgreSQL (production), SQLite (dev), Python 3.x, Metabase (analytics)

## Architecture & Data Model

### Core Business Apps (in dependency order)
1. **products**: Brand, ProductCategory, ProductType, Product - the inventory base
2. **suppliers**: Supplier, SupplierPayment - procurement source
3. **customers**: CustomerType, Customer, NoSaleReason, CustomerFollowUp - sales targets
4. **orders**: Order, OrderItem - sales transactions (links customers + products)
5. **stocks**: ProductReconciliation, CustomerReconciliation - inventory/receivable adjustments
6. **accounts**: Employee, Salary, Attendance, Leave, Holiday - HR management
7. **finances**: ExpenseType, Expense - cost tracking
8. **mobilebankings**: Mobile payment records (see migrations)
9. **data_imports**: Bulk import infrastructure (management commands in progress)
10. **analytics**: Metabase dashboard embedding (staff-only views)

### Key Design Patterns
- **ForeignKey on_delete=PROTECT**: Critical for referential integrity (Salary→Employee, Order→Customer). Prevents accidental data loss.
- **related_name**: Always used for reverse relations (e.g., `customer.orders.all()`, `employee.salaries.all()`)
- **Constants in common.constants**: All choice fields centralized (DISTRICT_CHOICES, COUNTRY_CHOICES, PRODUCT_STATUS_CHOICES, ORDER_STATUS_CHOICES, etc.)
- **Timestamps**: Every model has `created_at` (auto_now_add) and `updated_at` (auto_now)
- **Unique constraints**: Used in ProductReconciliation and SupplierPayment for data consistency

### Data Flow
Orders (sales) → Customer receivables | Orders require Products (stock) ← Supplier payments → Finances (expenses vs revenue)

## Development Workflow

### Setup
```bash
python manage.py migrate              # Apply all pending migrations
python manage.py createsuperuser      # Create admin user
python manage.py runserver            # Start dev server on http://127.0.0.1:8000
```

### Database Configuration
- Uses environment variables: `ENGINE`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`
- `.env` file required for secrets (`SECRET_KEY`, `METABASE_SECRET_KEY`, `METABASE_SITE_URL`)
- Production: PostgreSQL (psycopg2-binary installed)
- Development: SQLite or PostgreSQL

### Creating Models
1. Define in `{app}/models.py` with proper `on_delete` policies
2. Run: `python manage.py makemigrations {app}`
3. Verify migration in `{app}/migrations/NNNN_description.py`
4. Run: `python manage.py migrate`
5. Register in `{app}/admin.py` for Django admin access

### Testing & Data Validation
- Tests go in `{app}/tests.py`
- Model `.save()` overrides: rarely used; prefer Django's validators
- Decimal fields: used for monetary values (gross_amount, discount in Order; amount in SupplierPayment)
- Integer fields: used for counts/simpler amounts (salary, expense_amount, profit, adjust_amount)

## Project Conventions

### Model Metadata
```python
class Meta:
    ordering = ['name']  # Default sort in admin
    verbose_name = "Singular"  # Display name
    verbose_name_plural = "Plurals"
    constraints = [UniqueConstraint(...)]  # Database-level constraints
```

### Choice Fields
Always use constants from `common.constants`:
- DISTRICT_CHOICES: Bangladesh districts (63 entries, used in Customer, Supplier)
- COUNTRY_CHOICES: Import source countries
- PRODUCT_STATUS_CHOICES: ['active', 'inactive', 'out_of_stock']
- ORDER_STATUS_CHOICES: ['complete', 'return', 'cancel']
- MEASUREMENT_UNIT_CHOICES: ['Piece', 'Inch', 'Meter', 'Feet', 'Packet']

### Admin Access
- `/admin/` - Django admin (not heavily customized yet)
- `/admin/analytics/` - Metabase dashboard embed (requires @staff_member_required decorator)
- Metabase integration in `analytics/utils.py` uses JWT signing with 1-hour expiry

## Integration Points

### External Dependencies
- **Metabase**: Dashboard visualization (dashboard_id=3 referenced in views)
- **PostgreSQL**: Production database
- **gunicorn**: Production WSGI server
- **python-dotenv**: Environment variable management

### CSRF & Security
- ALLOWED_HOSTS: ['95.217.7.154', '127.0.0.1', 'localhost', 'jonaki.insafee.com', 'www.jonaki.insafee.com']
- CSRF_TRUSTED_ORIGINS: HTTPS domain list (jonaki.insafee.com)
- SECURE_PROXY_SSL_HEADER: Configured for reverse proxy (HTTP_X_FORWARDED_PROTO)

## Common Tasks

### Adding a New Requirement to an Existing Model
1. Add field to model in `{app}/models.py` with `null=True, blank=True` if optional
2. `makemigrations` → `migrate`
3. (Optional) Register in `{app}/admin.py` with fieldsets

### Querying Across Apps
- Orders with customer details: `Order.objects.select_related('customer', 'customer__customer_type')`
- Employee payroll: `Employee.objects.prefetch_related('salaries')`
- Product sales history: `Product.objects.prefetch_related('orderitem_set')`

### Debugging Model Issues
- Check `app/migrations/` for schema version mismatches
- Verify on_delete behavior: PROTECT prevents deletion, CASCADE deletes children
- Use `python manage.py sqlmigrate app migration_number` to see raw SQL

## Red Flags & Gotchas
- **Modifying existing migrations**: Never edit `.py` files in migrations/ directly; create new migrations
- **Missing related_name**: Always specify or reverse lookups fail (e.g., `employee.salary_set` instead of `employee.salaries`)
- **Type inconsistency**: Order.sale_amount is Integer, SupplierPayment.amount is Decimal - be intentional about which one to use
- **ProductReconciliation uniqueness**: Composite unique constraint on (product, reconciliation_date, updated_amount); audit carefully
