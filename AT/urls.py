from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from users import views as user_views
from core import views as core_views

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    path('', include('users.urls')),


    # Authentification
    path('signup/', user_views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Dashboard
    path('dashboard/', core_views.dashboard, name='dashboard'),

    # Apps
    path('clients/', include('core.urls')),   # routes clients
    path('invoices/', include('core.urls')),  # routes invoices

    # Page d'accueil (index)
    path('', core_views.index, name='index'),
]
