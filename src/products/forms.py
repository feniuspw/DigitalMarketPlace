from django import forms

from .models import Product
from django.utils.text import slugify
PUBLISH_CHOICES = (
    ('publish', "Publish"),
    ('draft', "Draft"),
)


# Hard way to create Forms
class ProductAddForm(forms.Form):
    title = forms.CharField(label='Label changing test (Title)', widget=forms.TextInput(
            attrs={
                "class": "my-custom-class",
                "placeholder": "Product Title",
            }
    ))
    description = forms.CharField(widget=forms.Textarea(
        attrs={"class": "my-custom-class",
               "placeholder": "Put the description here.",

               }
    ))
    price = forms.DecimalField(widget=forms.NumberInput(
        attrs={
            "class": "my-custom-class",
            "placeholder": "Product Price"
        }
    ))
    publish = forms.ChoiceField(widget=forms.RadioSelect, choices=PUBLISH_CHOICES, required=False)

    def clean_price(self):
        price = self.cleaned_data.get("price")
        if price <= 1.00:
            raise forms.ValidationError("Price must be greater than $1")
        elif price >= 100.00:
            raise forms.ValidationError("Price must be less than $100")
        return price

    def clean_title(self):
        title = self.cleaned_data.get("title")
        if len(title) > 3:
            return title
        else:
            raise forms.ValidationError("Title must be greater than 3 characters long.")


# Easy way to create forms
class ProductModelForm(forms.ModelForm):
    tags = forms.CharField(label='Related Tags', required=False)
    publish = forms.ChoiceField(widget=forms.RadioSelect, choices=PUBLISH_CHOICES, required=False)

    class Meta:
        model = Product
        fields = [
            "title",
            "description",
            "price",
            "media",
        ]
        widgets = {
            "title": forms.TextInput(attrs={
                "class": "my-custom-class",
                "placeholder": "Product Title",}),
            "description": forms.Textarea(attrs={
                "class": "my-custom-class",
                "placeholder": "Put the description here."}),
        }

    # We are going to override the clean method in order to make validations
    #def clean(self, *args, **kwargs):
        # run the default clean method
        #cleaned_data = super(ProductModelForm, self).clean(*args, **kwargs)
        #title = cleaned_data.get("title")
        #slug = slugify(title)
        #qs = Product.objects.filter(slug=slug).exists()
        #if qs:
        #    raise forms.ValidationError("Title is taken. A new title is needed. Please try again.")
        #return cleaned_data

    def clean_price(self):
        price = self.cleaned_data.get("price")
        if price <= 0:
            raise forms.ValidationError("Price must be greater than $0")
        return price

    def clean_title(self):
        title = self.cleaned_data.get("title")
        if len(title) > 3:
            return title
        else:
            raise forms.ValidationError("Title must be greater than 3 characters long.")


