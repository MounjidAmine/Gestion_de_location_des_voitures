# Importation des modules nécessaires pour la création des modèles
from django.db import models
from django.contrib.auth import get_user_model

# Récupération du modèle User par défaut de Django
User = get_user_model()

# Définition du modèle Client
class Client(models.Model):
    # Création d'une relation un-à-un avec le modèle User
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Champ pour stocker le nombre de voitures associées au client
    nombre_de_voiture = models.CharField(max_length=255)
    # Autres champs pour stocker des informations supplémentaires sur le client
    date_naissance = models.DateField(null=True, blank=True)
    adress = models.CharField(max_length=100, null=True, blank=True)
    telphone = models.CharField(max_length=10, null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True)
    is_user_authenticated = models.CharField(max_length=10, null=True, blank=True)
    last_activity = models.DateTimeField(blank=True, null=True)
    creation_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    # Méthode pour représenter l'objet Client sous forme de chaîne de caractères
    def __str__(self):
        return self.nombre_de_voituren 

class Employe(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telphone = models.CharField(max_length=10)
    date_naissance=models.DateField(null=True, blank=True)
    dateembauche=models.DateField(null=True, blank=True)
    adress=models.CharField(max_length=255)
    role=models.CharField(max_length=25)
    gender=models.CharField(max_length=10,null=True, blank=True)
    is_user_authenticated = models.CharField(max_length=10,null=True, blank=True)
    last_activity = models.DateTimeField(blank=True, null=True)
    creation_date = models.DateTimeField(auto_now_add=True,null=True, blank=True)

    def __str__(self):
        return self.user.username
    
class Vechule(models.Model):
    client = models.ForeignKey(Client, null=True, blank=True, on_delete=models.SET_NULL)
    immatriculation= models.CharField(max_length=30)
    modele= models.CharField(max_length=255)
    genre=models.CharField(max_length=30)
    puissance=models.CharField(max_length=30)
    livraison= models.DateField(null=True, blank=True)
    fin_liv= models.DateField(null=True, blank=True)
    km=models.CharField(max_length=100)
    gam=models.CharField(max_length=100)
    date_naiss=models.DateField(null=True, blank=True)
    cas=models.CharField(max_length=20,null=True, blank=True)
    def __str__(self):
        return f"{self.immatriculation} - {self.modele}"
    
class Remplacementvechule(models.Model):
    vechule=models.OneToOneField(Vechule, null=True, blank=True, on_delete=models.SET_NULL)
    client = models.ForeignKey(Client, null=True, blank=True, on_delete=models.SET_NULL)
    issuetype=models.CharField(max_length=50,null=True, blank=True)
    gam=models.CharField(max_length=40,null=True, blank=True)
    status=models.CharField(max_length=40,null=True, blank=True)
    date=models.DateField(null=True, blank=True)
    otherrequests=models.CharField(max_length=100,null=True, blank=True)
    dateincident=models.DateField(null=True, blank=True)
    lieu_incident=models.CharField(max_length=40,null=True, blank=True)
    Description=models.CharField(max_length=1000000000000,null=True, blank=True)
    type_de_reparation=models.CharField(max_length=40,null=True, blank=True)
    date_envoi = models.DateTimeField(auto_now_add=True)
    historique=models.CharField(max_length=40,null=True, blank=True)
