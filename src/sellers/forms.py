from django import forms


# TODO: BUG: se o usuario nao marcar a checkbox abaixo e der submit, da pau
class NewSellerForm(forms.Form):
    agree = forms.BooleanField(label='Agree to Terms', widget= forms.CheckboxInput)
