from django import forms

class ProductPriceImportForm(forms.Form):
    csv_file = forms.FileField()