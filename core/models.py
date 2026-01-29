from django.db import models
from django.conf import settings

# -----------------------
# Client
# -----------------------
from django.db import models
from django.conf import settings

class Client(models.Model):
    SEX_CHOICES = [
        ('M', 'Masculin'),
        ('F', 'Féminin'),
        ('O', 'Autre'),
    ]

    PROVINCE_CHOICES = [
        ('province1', 'Antananarivo'),
        ('province2', 'Antsiranana'),
        ('province3', 'Toamasina'),
        ('province4', 'Mahajanga'),
        ('province5', 'Fianarantsoa'),
        ('province6', 'Toliara'),
        # Ajoute toutes les provinces nécessaires
    ]

    AGE_CHOICES = [
        ('<18', 'Moins de 18 ans'),
        ('18-25', '18-25 ans'),
        ('26-35', '26-35 ans'),
        ('36-50', '36-50 ans'),
        ('50+', 'Plus de 50 ans'),
    ]

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=50, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    # Nouveaux champs
    sex = models.CharField(max_length=1, choices=SEX_CHOICES, blank=True, null=True)
    province = models.CharField(max_length=50, choices=PROVINCE_CHOICES, blank=True, null=True)
    
    # Champ âge choisi directement
    age_range = models.CharField(
        max_length=10,
        choices=AGE_CHOICES,
        blank=True,
        null=True
    )

    @property
    def age_range_label(self):
        """Retourne la tranche d’âge du client en texte"""
        if not self.age_range:
            return "Inconnu"
        return dict(self.AGE_CHOICES).get(self.age_range, "Inconnu")

    def __str__(self):
        return self.name
    

# <- Nouveau champ pour la date de création
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    

# -----------------------
# Product
# -----------------------
class Product(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


# -----------------------
# Invoice
# -----------------------
class Invoice(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Brouillon'),
        ('sent', 'Envoyée'),
        ('paid', 'Payée'),
        ('cancelled', 'Annulée'),
    ]

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='InvoiceItem')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField(null=True, blank=True)

    @property
    def total(self):
        return sum(item.total() for item in self.invoiceitem_set.all())

    def __str__(self):
        return f"Facture {self.id} - {self.client.name}"


# -----------------------
# Invoice Item
# -----------------------
class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"







