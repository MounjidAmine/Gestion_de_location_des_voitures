# Importation des modules nécessaires de Django
from django.contrib import admin
# Importation des modèles définis dans models.py du même répertoire
from .models import Client, Employe, Vechule, Remplacementvechule

# Création d'une classe d'administration pour le modèle Client
class AdminClient(admin.ModelAdmin):
    # Définition des champs à afficher dans la liste des clients dans l'interface d'administration
    list_display = ('user', 'nombre_de_voiture')
    
# Création d'une classe d'administration pour le modèle Employe
class AdminEmploye(admin.ModelAdmin):
    # Définition des champs à afficher dans la liste des employés dans l'interface d'administration
    list_display = ('user', 'telphone', 'date_naissance', 'adress', 'role')

# Création d'une classe d'administration pour le modèle Vechule
class AdminVechule(admin.ModelAdmin):
    # Définition des champs à afficher dans la liste des véhicules dans l'interface d'administration
    list_display = ('client', 'immatriculation')

# Création d'une classe d'administration pour le modèle Remplacementvechule
class AdminRemplacement(admin.ModelAdmin):
    # Définition des champs à afficher dans la liste des remplacements de véhicules dans l'interface d'administration
    list_display = ('vechule', 'issuetype')

# Enregistrement des modèles avec leurs classes d'administration correspondantes pour les rendre accessibles dans l'interface d'administration de Django
admin.site.register(Employe, AdminEmploye)
admin.site.register(Client, AdminClient)
admin.site.register(Vechule, AdminVechule)
admin.site.register(Remplacementvechule, AdminRemplacement)
