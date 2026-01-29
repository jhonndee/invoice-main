from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_admin, name='dashboard_admin'),
    path('users/', views.user_list, name='user_list'),
    path('users/<int:pk>/detail/', views.user_detail, name='user_detail'),
    path('users/<int:pk>/toggle-active/', views.toggle_active, name='toggle_active'),
    path('subscriptions/', views.subscription_list, name='subscription_list'),
]
