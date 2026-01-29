from django.urls import path
from . import views

urlpatterns = [
    # Dashboard
    #path('', views.dashboard, name='dashboard'),
    #path('admin-dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/', views.dashboard, name='dashboard'),

    # Clients CRUD
    path('clients/', views.client_list, name='client_list'),
    path('clients/add/', views.client_create, name='client_create'),
    path('clients/<int:pk>/edit/', views.client_edit, name='client_edit'),
    path('clients/<int:pk>/delete/', views.client_delete, name='client_delete'),

    # Factures CRUD
    path('invoices/', views.invoice_list, name='invoice_list'),
    path('invoices/add/', views.invoice_create, name='invoice_create'),
    path('invoices/<int:pk>/edit/', views.invoice_edit, name='invoice_edit'),
    path('invoices/<int:pk>/delete/', views.invoice_delete, name='invoice_delete'),
    path('invoices/<int:pk>/pdf/', views.invoice_pdf, name='invoice_pdf'),
    #path('invoices/new/', views.invoice_create, name='invoice_create'),  # <- ici
    #path('invoices/', views.invoice_list, name='invoice_list'),
    path('clients/stats/', views.clients_stats, name='clients_stats'),
    path('invoice/<int:pk>/', views.invoice_detail, name='invoice_detail'),
]
