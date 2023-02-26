from django import forms
from django.utils.translation import gettext_lazy as _
from decimal import Decimal

from .models import *


class CustomMMCF(forms.ModelMultipleChoiceField):
    def label_from_instance(self, Categories) -> str:
        return f"{Categories.name}"

class CreateListingForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['prod_name', 'price_base', 'image_path', 'description', 'category']
        exclude = ['date_created', 'price_cur', 'seller']
        labels = {
            'price_base': _('Price*'),
            'image_path': _('Image*'),
            'description': _('Brief description'),
            'category': _('Catgories')
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
        self.fields['price_base'].min_value = Decimal('0.01')
        self.fields['image_path'].widget = forms.ClearableFileInput(attrs={
            "class": "ms-2"
        })
        self.fields['description'].widget = forms.Textarea(attrs={
            "class": "form-control ms-2"
        })

    category = CustomMMCF(
        queryset=Categories.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={
            "class": "ms-2"
        })
    )


class BidForm(forms.ModelForm):
    bid_price = forms.DecimalField(min_value=Decimal('0.01'),
                                   max_digits=19, decimal_places=4,
                                   widget=forms.NumberInput(attrs={
                                        'placeholder': 'Bid',
                                        'class': 'form-control mb-1',
                                        'aria-label': 'bid price',
                                        'name': 'bid_price'
                                    }))

    class Meta:
        model = Bidinglist
        fields = ['bid_price']
        exclude = ['user', 'product', 'bid_time']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['comment']
        exclude = ['user', 'product', 'date_added']
        widgets = {
            'comment': forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": "Write your comment"
            })
        }
        labels = {
            'comment': ''
        }