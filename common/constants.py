DISTRICT_CHOICES = (
        ('Bagerhat', 'Bagerhat'),
        ('Bandarban', 'Bandarban'),
        ('Barguna', 'Barguna'),
        ('Barishal', 'Barishal'),
        ('Bhola', 'Bhola'),
        ('Bogura', 'Bogura'),
        ('Brahmanbaria', 'Brahmanbaria'),
        ('Chandpur', 'Chandpur'),
        ('Chapai Nawabganj', 'Chapai Nawabganj'),
        ('Chattogram', 'Chattogram'),
        ('Chuadanga', 'Chuadanga'),
        ('Comilla', 'Comilla'),
        ('Coxs Bazar', 'Coxs Bazar'),
        ('Cumilla', 'Cumilla'),
        ('Dhaka', 'Dhaka'),
        ('Dinajpur', 'Dinajpur'),
        ('Faridpur', 'Faridpur'),
        ('Feni', 'Feni'),
        ('Gaibandha', 'Gaibandha'),
        ('Gazipur', 'Gazipur'),
        ('Gopalganj', 'Gopalganj'),
        ('Habiganj', 'Habiganj'),
        ('Jamalpur', 'Jamalpur'),
        ('Jashore', 'Jashore'),
        ('Jhalokati', 'Jhalokati'),
        ('Jhenaidah', 'Jhenaidah'), 
        ('Joypurhat', 'Joypurhat'),
        ('Khagrachari', 'Khagrachari'),
        ('Khulna', 'Khulna'),
        ('Kishoreganj', 'Kishoreganj'),
        ('Kurigram', 'Kurigram'),
        ('Kushtia', 'Kushtia'),
        ('Lakshmipur', 'Lakshmipur'),
        ('Lalmonirhat', 'Lalmonirhat'),
        ('Madaripur', 'Madaripur'),
        ('Magura', 'Magura'),
        ('Manikganj', 'Manikganj'),
        ('Meherpur', 'Meherpur'),
        ('Moulvibazar', 'Moulvibazar'),
        ('Munshiganj', 'Munshiganj'),
        ('Mymensingh', 'Mymensingh'),
        ('Naogaon', 'Naogaon'),
        ('Narail', 'Narail'),
        ('Narayanganj', 'Narayanganj'),
        ('Narsingdi', 'Narsingdi'),
        ('Natore', 'Natore'),
        ('Netrokona', 'Netrokona'),
        ('Nilphamari', 'Nilphamari'),
        ('Noakhali', 'Noakhali'),
        ('Pabna', 'Pabna'),
        ('Panchagarh', 'Panchagarh'),
        ('Patuakhali', 'Patuakhali'),
        ('Pirojpur', 'Pirojpur'),
        ('Rajbari', 'Rajbari'),
        ('Rajshahi', 'Rajshahi'),
        ('Rangamati', 'Rangamati'),
        ('Rangpur', 'Rangpur'),
        ('Satkhira', 'Satkhira'),
        ('Shariatpur', 'Shariatpur'),
        ('Sherpur', 'Sherpur'),
        ('Sirajganj', 'Sirajganj'),
        ('Sunamganj', 'Sunamganj'),
        ('Sylhet', 'Sylhet'),
        ('Tangail', 'Tangail'),
        ('Thakurgaon', 'Thakurgaon')
)
COUNTRY_CHOICES = (
    ('Bangladesh', 'Bangladesh'),
    ('India', 'India'),
    ('China', 'China'),
    ('Japan', 'Japan'),
    ('Korea', 'Korea'),
    ('Taiwan', 'Taiwan')
)

MEASUREMENT_UNIT_CHOICES = (
        ('Piece', 'Piece'),
        ('Inch', 'Inch'),
        ('Meter', 'Meter'),
        ('Feet', 'Feet'),
        ('Packet', 'Packet')
)

PRODUCT_STATUS_CHOICES = [
    ('active', 'Active'),
    ('inactive', 'Inactive'),
    ('out_of_stock', 'Out of Stock'),
]

ORDER_STATUS_CHOICES = [
    ('complete', 'Complete'),
    ('return', 'Return'),
    ('cancel', 'Cancel'),
]

NO_SALE_REASON_CHOICES = [
        ('PRICE_HIGH', 'Price Too High'),
        ('NO_STOCK', 'Product Not Available'),
        ('INQUIRY', 'Inquiry Only'),
        ('COMPARE', 'Comparing Prices'),
        ('LATER', 'Will Buy Later'),
        ('LEFT_WITHOUT_REASON', 'Left Without Reason'),
        ('OUT_OF_BUDGET', 'Out of Budget'),
        ('WRONG_SPECIFICATION', 'Wrong Specification'),
        ('ANOTHER_BRAND', 'Looking for Another Brand'),
        ('URGENT_NEED_NOT_MET', 'Urgent Need Not Met'),
        ('OTHER', 'Other'),
]

FINANCIAL_RECONCILIATION_CATEGORY_CHOICES = [
    ('cash', 'Cash'),
    ('bank', 'Bank'),
    ('others', 'Others'),
]

MOBILE_BANKING_CATEGORY_CHOICES = [
    ('BKASH', 'bKash'),
    ('NAGAD', 'Nagad'),
    ('ROCKET', 'Rocket'),
    ('BKASHPERSONAL', 'Bkash Personal'),
    ('NAGADPERSONAL', 'Nagad Personal'),
    ('ROCKETPERSONAL', 'Rocket Personal'),
    ('UPAY', 'Upay'),
    ('SURECASH', 'SureCash'),
    ('MCASH', 'mCash'),
    ('FLATBELT', 'Flatbelt'),
    ('OTHER', 'Other'),
]

LEAVE_REASON_CHOICES = [
        ('SICK', 'Sick Leave'),
        ('FAMILYSICK', 'Family Sick Leave'),
        ('CASUAL', 'Casual or personal Leave'),
        ('OTHER', 'Other'),
]

CONTACT_TYPE_CHOICES = [
        ('phone', 'Phone'),
        ('email', 'Email'),
]

RESPONSE_TYPE_CHOICES = [
    ('received', 'Call Received'),
    ('not_received', 'Call Not Received'),
    ('busy', 'Busy'),
    ('switched_off', 'Switched Off'),
    ('wrong_number', 'Wrong Number'),

    # Positive / Active customer states
    ('regular_customer', 'Regular Customer'),
    ('repeat_order', 'Repeat Order Confirmed'),
    ('visited_shop', 'Visited Shop'),

    # Sales intent
    ('interested', 'Interested'),
    ('not_interested', 'Not Interested'),
    ('call_later', 'Asked to Call Later'),
]

FIXED_HOLIDAY_CHOICES = [
    ('Shab-e-Barat', 'Shab-e-Barat'), 
    ('Eid-e-Milad-un-Nabi', 'Eid-e-Milad-un-Nabi'), 
    ('Pohela Boishakh', 'Pohela Boishakh'),
    ('Shaheed Dibosh & International Mother Language Day', 'Shaheed Dibosh & International Mother Language Day'),
    ('Shab-e-Qadr', 'Shab-e-Qadr'),
    ('Independence Day', 'Independence Day'), 
    ('May Day', 'May Day'), 
    ('Eid al-Fitr', 'Eid al-Fitr'), 
    ('Eid al-Adha', 'Eid al-Adha'), 
    ('Durga Puja', 'Durga Puja'),
    ('July Mass-uprising Day', 'July Mass-uprising Day'),
    ('Janmashtami', 'Janmashtami'),  
    ('Buddha Purnima', 'Buddha Purnima'), 
    ('Christmas Day', 'Christmas Day'),
    ('Victory Day', 'Victory Day'),
    ('Condolence', 'Condolence'),
    ('Others', 'Others')
]

INVEST_TYPE_CHOICES = [
    ('Invest', 'Invest'), 
    ('Haolad', 'Haolad'),     
]