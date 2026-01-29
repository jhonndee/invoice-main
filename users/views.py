# users/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from .forms import CustomUserCreationForm

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # <-- Sauvegarde le nouvel utilisateur
            login(request, user)  # <-- Connecte l'utilisateur immédiatement
            messages.success(request, "Compte créé avec succès !")
            return redirect('dashboard')  # <-- redirige vers la page souhaitée
        else:
            messages.error(request, "Veuillez corriger les erreurs ci-dessous.")
    else:
        form = CustomUserCreationForm()

    return render(request, 'users/signup.html', {'form': form})
