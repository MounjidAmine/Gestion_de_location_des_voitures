# Importation des modules nécessaires de Django pour la gestion des formulaires
from django import forms  
from .models import Client  # Importation du modèle Client depuis models.py du même répertoire
from django.forms import fields  # Importation de fields de django.forms (cependant, cet import n'est pas utilisé directement dans le code fourni)
from django.contrib.auth.forms import UserChangeForm  # Importation de UserChangeForm pour créer des formulaires de modification de l'utilisateur
from django.contrib.auth.models import User  # Importation du modèle User intégré de Django pour la gestion des utilisateurs

# Création d'une classe de formulaire pour mettre à jour les informations de l'utilisateur
class UserUpdateForm(UserChangeForm):
    class Meta:
        model = User  # Spécifie que le modèle utilisé par ce formulaire est le modèle User
        fields = "__all__"  # Indique que tous les champs du modèle User doivent être inclus dans le formulaire

# Création d'une classe de formulaire pour le modèle Client
class ClientForm(forms.ModelForm):  
    class Meta:  
        model = Client  # Spécifie que le modèle utilisé par ce formulaire est le modèle Client
        fields = ['user', 'nombre_de_voiture']  # Définit les champs du modèle Client qui doivent être inclus dans le formulaire
