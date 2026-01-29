# api/index.py

"""
Entrypoint pour Vercel
Ce fichier permet à Vercel de servir votre projet Django.
"""

import os
from AT.wsgi import application as app  # importe le WSGI callable

# Si tu veux, tu peux définir ici des variables d'environnement pour Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "AT.settings")

# app est le callable que Vercel va utiliser
# Ne rien changer ici : Vercel attend 'app'
