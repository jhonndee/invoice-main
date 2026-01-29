from django.contrib import admin

# Register your models here.
from .models import Client, Product, Invoice, InvoiceItem

# Inline pour afficher InvoiceItem dans la page de facture
class InvoiceItemInline(admin.TabularInline):
    model = InvoiceItem
    extra = 1

# Admin de Invoice avec les produits en inline
class InvoiceAdmin(admin.ModelAdmin):
    inlines = [InvoiceItemInline]
    list_display = ('id', 'client', 'status', 'created_at')

admin.site.register(Client)
admin.site.register(Product)
admin.site.register(Invoice, InvoiceAdmin)
