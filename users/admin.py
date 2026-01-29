from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from django.contrib import admin


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser

    # Champs affichés dans la liste des utilisateurs
    list_display = (
        "username",
        "email",
        "phone",
        "company_name",
        "statut",
        "is_client",
        "is_staff",
        "is_active",
    )

    # Filtres à droite
    list_filter = (
        "statut",
        "is_client",
        "is_staff",
        "is_active",
    )

    # Champs de recherche
    search_fields = (
        "username",
        "email",
        "phone",
        "company_name",
    )

    ordering = ("username",)

    # Organisation du formulaire dans l’admin
    fieldsets = (
        (None, {
            "fields": ("username", "password")
        }),
        ("Informations personnelles", {
            "fields": (
                "first_name",
                "last_name",
                "email",
                "phone",
                "company_name",
                "statut",
                "is_client",
            )
        }),
        ("Permissions", {
            "fields": (
                "is_active",
                "is_staff",
                "is_superuser",
                "groups",
                "user_permissions",
            )
        }),
        ("Dates importantes", {
            "fields": ("last_login", "date_joined")
        }),
    )

    # Champs lors de la création d’un utilisateur via l’admin
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "username",
                "email",
                "phone",
                "company_name",
                "statut",
                "is_client",
                "password1",
                "password2",
                "is_staff",
                "is_active",
            ),
        }),
    )



admin.site.site_header = "Administration MyProject"
admin.site.site_title = "MyProject Admin"
admin.site.index_title = "Tableau de bord"
from django.contrib import admin

class GlobalAdmin(admin.ModelAdmin):
    class Media:
        css = {
            "all": ("admin/css/custom_admin.css",)
        }

admin.site.site_header = "Admin MyProject"
