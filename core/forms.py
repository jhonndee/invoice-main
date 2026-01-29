from django import forms
from django import forms
from .models import CompanyProfile
from .models import Client, Product, Invoice

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['client', 'status', 'due_date']

class ProductSelectionForm(forms.Form):
    product_id = forms.IntegerField(widget=forms.HiddenInput)
    quantity = forms.IntegerField(min_value=1, initial=1)



class CompanyProfileForm(forms.ModelForm):
    class Meta:
        model = CompanyProfile
        fields = ['company_name', 'address', 'email', 'phone', 'logo']
        widgets = {
            'address': forms.Textarea(attrs={
                'rows': 3,          # 👈 hauteur réduite
                'placeholder': 'Adresse de l’entreprise'
            }),
        }

