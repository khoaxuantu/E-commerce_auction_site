from django import forms
from django.utils.translation import gettext_lazy as _

from .models import *

class CreateListingForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['prod_name', 'price_base', 'image_path', 'description']
        exclude = ['date_created', 'price_cur', 'bids', 'seller', 'category']
        labels = {
            'price_base': _('Price*'),
            'image_path': _('Image*'),
            'description': _('Brief description')
        }

    def __init__(self, *args, **kwargs):
        super(CreateListingForm, self).__init__(*args, **kwargs)
        self.fields['prod_name'].widget = forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Product name*",
            "aria-label": "product name",
            "name": "product_name"
        })
        self.fields['price_base'].widget = forms.NumberInput(attrs={
            "class": "form-control ms-2",
            "aria-label": "listing price",
            "name": "price"
        })
        self.fields['image_path'].widget = forms.ClearableFileInput(attrs={
            "class": "ms-2"
        })
        self.fields['description'].widget = forms.Textarea(attrs={
            "class": "form-control ms-2"
        })
