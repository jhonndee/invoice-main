from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Client, Invoice, Product, InvoiceItem
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.shortcuts import render, get_object_or_404
from .models import Invoice





def invoice_detail(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)

    items = invoice.invoiceitem_set.all()  # liste des produits avec quantité
    total = invoice.total  # total calculé

    return render(request, "core/invoice_detail.html", {

        "invoice": invoice,
        "items": items,
        "total": total
    })



@login_required
def company_settings(request):
    company, created = CompanyProfile.objects.get_or_create(
        user=request.user
    )

    if request.method == "POST":
        form = CompanyProfileForm(request.POST, request.FILES, instance=company)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = CompanyProfileForm(instance=company)

    return render(request, "core/company_settings.html", {
        "form": form
    })




# ----------------- DASHBOARD -----------------
@login_required
def dashboard(request):
    invoices_count = Invoice.objects.filter(owner=request.user).count()
    clients_count = Client.objects.filter(owner=request.user).count()
    return render(request, 'core/dashboard.html', {
        'invoices_count': invoices_count,
        'clients_count': clients_count,
    })

# ----------------- CLIENTS CRUD -----------------
@login_required
def client_list(request):
    clients = Client.objects.filter(owner=request.user)
    return render(request, 'core/client_list.html', {'clients': clients})

@login_required
def client_create(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST.get('phone', '')
        address = request.POST.get('address', '')
        Client.objects.create(owner=request.user, name=name, email=email, phone=phone, address=address)
        return redirect('client_list')
    return render(request, 'core/client_form.html')

@login_required
def client_edit(request, pk):
    client = get_object_or_404(Client, pk=pk, owner=request.user)
    if request.method == 'POST':
        client.name = request.POST['name']
        client.email = request.POST['email']
        client.phone = request.POST.get('phone', '')
        client.address = request.POST.get('address', '')
        client.save()
        return redirect('client_list')
    return render(request, 'core/client_form.html', {'client': client})

@login_required
def client_delete(request, pk):
    client = get_object_or_404(Client, pk=pk, owner=request.user)
    client.delete()
    return redirect('client_list')

# ----------------- INVOICES CRUD -----------------
@login_required
def invoice_list(request):
    invoices = Invoice.objects.filter(owner=request.user)
    return render(request, 'core/invoice_list.html', {'invoices': invoices})


# ----------------- INVOICES CReat -----------------
@login_required
def invoice_create(request):
    clients = Client.objects.filter(owner=request.user)

    if request.method == 'POST':
        client_id = request.POST['client']
        client = get_object_or_404(Client, pk=client_id, owner=request.user)

        status = request.POST.get('status', 'draft')

        # gérer la date correctement
        due_date_str = request.POST.get('due_date')
        due_date = due_date_str if due_date_str else None

        invoice = Invoice.objects.create(
            owner=request.user,
            client=client,
            status=status,
            due_date=due_date
        )

        # produits libres
        names = request.POST.getlist("free_product_name[]")
        prices = request.POST.getlist("free_product_price[]")
        qtys = request.POST.getlist("free_product_quantity[]")

        for name, price, qty in zip(names, prices, qtys):
            if name.strip():  # ignorer les lignes vides
                try:
                    price = float(price) if price else 0
                    qty = int(qty) if qty else 1

                    temp_product = Product.objects.create(
                        owner=request.user,
                        name=name,
                        price=price
                    )

                    InvoiceItem.objects.create(
                        invoice=invoice,
                        product=temp_product,
                        quantity=qty
                    )
                except ValueError:
                    continue

        return redirect('invoice_list')

    return render(request, 'core/invoice_form.html', {'clients': clients})


@login_required
def invoice_edit(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk, owner=request.user)
    clients = Client.objects.filter(owner=request.user)
    products = Product.objects.filter(owner=request.user)
    if request.method == 'POST':
        client_id = request.POST['client']
        invoice.client = get_object_or_404(Client, pk=client_id, owner=request.user)
        invoice.invoiceitem_set.all().delete()
        for product_id, qty in zip(request.POST.getlist('product'), request.POST.getlist('quantity')):
            product = get_object_or_404(Product, pk=product_id, owner=request.user)
            InvoiceItem.objects.create(invoice=invoice, product=product, quantity=int(qty))
        invoice.save()
        return redirect('invoice_list')
    return render(request, 'core/invoice_form.html', {'invoice': invoice, 'clients': clients, 'products': products})

@login_required
def invoice_delete(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk, owner=request.user)
    invoice.delete()
    return redirect('invoice_list')

# ----------------- EXPORT PDF -----------------
@login_required
def invoice_pdf(request, pk):
    """
    Génère un PDF pour une facture donnée en utilisant xhtml2pdf.
    """
    # Récupérer la facture correspondant à l'utilisateur connecté
    invoice = get_object_or_404(Invoice, pk=pk, owner=request.user)
    
    # Charger le template HTML et le rendre avec les données de la facture
    template = get_template('core/invoice_pdf.html')
    html = template.render({'invoice': invoice})
    
    # Créer une réponse HTTP avec le bon type de contenu
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename="facture_{invoice.id}.pdf"'
    
    # Générer le PDF
    pisa_status = pisa.CreatePDF(html, dest=response)
    
    # Vérifier si une erreur est survenue lors de la génération
    if pisa_status.err:
        return HttpResponse("Erreur lors de la génération du PDF")
    
    # Retourner la réponse contenant le PDF
    return response



# ----------------- STATS CLIENTS -----------------
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.db.models.functions import TruncMonth
from .models import Client

from django.db.models.functions import TruncMonth

@login_required
def clients_stats(request):
    from collections import Counter
    from django.db.models import Count

    clients_qs = Client.objects.filter(owner=request.user)

    # --- Clients par province ---
    clients_by_province_qs = clients_qs.values('province') \
                                      .annotate(count=Count('id')) \
                                      .order_by('province')
    clients_by_province_labels = [entry['province'] or "Inconnu" for entry in clients_by_province_qs]
    clients_by_province_data = [entry['count'] for entry in clients_by_province_qs]

    # --- Clients par tranche d'âge ---
    age_ranges = [client.age_range or "Inconnu" for client in clients_qs]
    age_counter = Counter(age_ranges)
    clients_by_age_labels = list(age_counter.keys())
    clients_by_age_data = list(age_counter.values())

    # --- Clients par mois (created_at) ---
    clients_by_month_qs = clients_qs.annotate(month=TruncMonth('created_at')) \
                                    .values('month') \
                                    .annotate(count=Count('id')) \
                                    .order_by('month')
    clients_by_month_labels = [entry['month'].strftime("%Y-%m") if entry['month'] else "Inconnu" for entry in clients_by_month_qs]
    clients_by_month_data = [entry['count'] for entry in clients_by_month_qs]

    context = {
        'clients_by_province_labels': clients_by_province_labels,
        'clients_by_province_data': clients_by_province_data,
        'clients_by_age_labels': clients_by_age_labels,
        'clients_by_age_data': clients_by_age_data,
        'clients_by_month_labels': clients_by_month_labels,
        'clients_by_month_data': clients_by_month_data,
    }

    return render(request, 'core/clients_stats.html', context)

def index(request):
    return render(request, 'index.html')
