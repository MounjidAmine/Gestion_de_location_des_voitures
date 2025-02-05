from django.shortcuts import render
from django.shortcuts import redirect, render,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Client,Employe,Vechule,Remplacementvechule
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import re
from datetime import datetime, timedelta
from django.urls import reverse
from django.contrib.auth.decorators import user_passes_test,login_required

def accueil(request):
    return render(request, 'pfm/test/index.html')
def admin_required(view_func):   
     # Décorateur pour exiger que l'utilisateur soit un administrateur (superuser)
    decorated_view_func = login_required(user_passes_test(lambda user: user.is_superuser)(view_func))
    return decorated_view_func

def client_required(view_func):
     # Décorateur pour exiger que l'utilisateur soit un client (basé sur le modèle Client)
    decorated_view_func = login_required(user_passes_test(lambda user: Client.objects.filter(user=user).exists())(view_func))
    return decorated_view_func

def employe_required(view_func):
    # Décorateur pour exiger que l'utilisateur soit un employé (basé sur le modèle Employe)
    decorated_view_func = login_required(user_passes_test(lambda user: Employe.objects.filter(user=user).exists())(view_func))
    return decorated_view_func
#-----------------------------------------------------------------------------------------------------------------------------------------#
#-----------------------------------------------------------------------------------------------------------------------------------------#
#-----------------------------------------------------------------------------------------------------------------------------------------#
#                                                                                                                                         #
#                                                         Admin                                                                           #
#                                                                                                                                         #
#-----------------------------------------------------------------------------------------------------------------------------------------#
#-----------------------------------------------------------------------------------------------------------------------------------------#
#-----------------------------------------------------------------------------------------------------------------------------------------#
def est_administrateur(user):
    return user.is_superuser
def home(request):
    return render(request,"index.html")
from datetime import datetime, timedelta
from django.utils import timezone
from threading import Timer

def showdashboard(request):
    clients = Client.objects.all()
    employes = Employe.objects.all()
    client_number = len(clients)
    employe_number = len(employes)
    total = employe_number + client_number
    return render(request, "pfm/test/dashboard.html", {
        'clients': clients,
        'employes': employes,
        'client_number': client_number,
        'employe_number': employe_number,
        'total': total
    })

def managerequest(request):
    remplacement=Remplacementvechule.objects.all()
    return render(request,"pfm/test/managerequest.html",{"remplacements":remplacement})


#------------------------------------------------------------------------------------------------------------------------------------------#
def is_integer(value):
    try:
        int(value)
        return True
    except ValueError:
        return False
#------------------------------------------------------------------------------------------------------------------------------------------#
def is_valid_name(value):
    pattern = r'^[A-Za-z]+$'
    return re.match(pattern, value) is not None
#------------------------------------------------------------------------------------------------------------------------------------------#
def password_filter(password):
    # Vérifie si un mot de passe est conforme aux critères spécifiés (longueur, caractères majuscules et minuscules, chiffres)
    if len(password) < 8:
        return False
    if not re.search('[A-Z]', password):
        return False
    if not re.search('[a-z]', password):
        return False
    if not re.search('[0-9]', password):
        return False
    return True
#-----------------------------------------------------------------------------------------------------------------------------------------#
#                                                                                                                                         #
#                                                          Partie client                                                                  #
#                                                                                                                                         #
#-----------------------------------------------------------------------------------------------------------------------------------------#
#                                                             CRUD                                                                        #      
#-----------------------------------------------------------------------------------------------------------------------------------------#
def register(request):
     # Récupération des données du formulaire
    if request.method == "POST":
        username = request.POST['username']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        password = request.POST['password']
        confirmpwd = request.POST['comfirmpwd']
        nbr_voiture = request.POST['nombre_voiture']        
        #--------------------------------------------------------partie filtre----------------------------------------------------------#
        # Validation des données
        if not username.isalnum():
            messages.error(request, "Le nom d'utilisateur n'est pas valide. Utilisez uniquement des lettres et des chiffres.")
            return redirect("register")
        
        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, "L'adresse email n'est pas valide.")
            return redirect("register")
        
        if not is_valid_name(firstname):
            messages.error(request, "Le prénom n'est pas valide. Utilisez uniquement des lettres.")
            return redirect("register")
        
        if not is_valid_name(lastname):
            messages.error(request, "Le nom de famille n'est pas valide. Utilisez uniquement des lettres.")
            return redirect("register")
        
        if not password_filter(password):
            messages.error(request, "mot de passe doit avoir 8 carctere, avoir majuscule miniscule nombre est des carctere ")
        
        if not is_integer(nbr_voiture):
            messages.error(request, "Le nombre de voitures doit être un nombre entier.")
            return redirect("register")
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "Le nom d'utilisateur existe déjà.")
            return redirect("register")
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "L'adresse email existe déjà.")
            return redirect("register")
        
        if password != confirmpwd:
            messages.error(request, 'Le mot de passe ne correspondait pas ! ')  
            return redirect('register')     
        #-------------------------------------------------------------------------------------------------------------------------------------#
        # Création de l'utilisateur et du client si les validations réussissent
        my_user = User.objects.create_user(username, email, password)
        my_user.first_name =firstname
        my_user.last_name = lastname
        my_user.save()
        client = Client(user=my_user,nombre_de_voiture=nbr_voiture)
        client.save()
         # Affichage du formulaire d'enregistrement
        messages.success(request, 'Your account has been successfully created.')
    return render(request, 'pfm/test/createclient.html')  
#------------------------------------------------------------------------------------------------------------------------------------------#
def logIn(request):
    # Authentification de l'utilisateur
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']            
        user=authenticate(request,username=username,password=password)
        # Redirection vers le tableau de bord approprié en fonction du type de l'utilisateur
        if user is not None:
            login(request,user)
            if Client.objects.filter(user__username=username).exists():
                client = Client.objects.get(user=user)
                client.is_user_authenticated="True"
                client.save()
                return redirect('vechulefleet')
            elif Employe.objects.filter(user__username=username).exists():
                employe = Employe.objects.get(user=user)
                employe.is_user_authenticated="True"
                employe.save()
                return redirect('viewrequest')
            else:
                return redirect('dashboard')

        else:
            messages.error(request,'Mauvaise authentification')
            return redirect('login')
    return render(request,'pfm/test/login.html')
#------------------------------------------------------------------------------------------------------------------------------------------#   
def logOut(request):
    # Déconnexion de l'utilisateur et mise à jour du statut d'authentification
    if request.user.is_authenticated:
        if Client.objects.filter(user=request.user).exists():
            client = Client.objects.get(user=request.user)
            client.is_user_authenticated = None
            client.save()
        elif Employe.objects.filter(user=request.user).exists():
            employe = Employe.objects.get(user=request.user)
            employe.is_user_authenticated = None
            employe.save()
    
    logout(request)
    messages.success(request, 'Vous avez été bien déconnecté')
    return redirect('login')
#------------------------------------------------------------------------------------------------------------------------------------------#
def show(request):
    client=Client.objects.all()
    return render(request,"pfm/test/manageclient.html",{'clients':client})  
#------------------------------------------------------------------------------------------------------------------------------------------#
def edit(request, id):  
    client = get_object_or_404(Client,user__id=id) 
    return render(request,'pfm/test/modifieclient.html', {'clients':client})  
#------------------------------------------------------------------------------------------------------------------------------------------#
def update(request, id):  
    client = get_object_or_404(Client, user__id=id)
    if request.method == "POST":        
        username = request.POST['username']
        firstname = request.POST['first_name']
        lastname = request.POST['last_name']
        email = request.POST['email']
        nbr_voiture = request.POST['nombre_voiture']
        #--------------------------------------------------------partie filtre----------------------------------------------------------#
        if not username.isalnum():
            messages.error(request, "Le nom d'utilisateur n'est pas valide. Utilisez uniquement des lettres et des chiffres.")
            return redirect("show")
        
        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, "L'adresse email n'est pas valide.")
            return redirect("show")
        
        if not is_valid_name(firstname):
            messages.error(request, "Le prénom n'est pas valide. Utilisez uniquement des lettres.")
            return redirect("show")
        
        if not is_valid_name(lastname):
            messages.error(request, "Le nom de famille n'est pas valide. Utilisez uniquement des lettres.")
            return redirect("show")
        
        if not is_integer(nbr_voiture):
            messages.error(request, "Le nombre de voitures doit être un nombre entier.")
            return redirect("show")
        
        if User.objects.exclude(id=client.user.id).filter(username=username).exists() and username != client.user.username:
            messages.error(request, "Le nom d'utilisateur existe déjà.")
            return redirect("show")
        
        if User.objects.exclude(id=client.user.id).filter(email=email).exists() and email != client.user.email:
            messages.error(request, "L'adresse email existe déjà.")
            return redirect("show")
#-----------------------------------------------------------------------------------------------------------------------------------#
        client.user.username=username  
        client.user.first_name=firstname
        client.user.last_name=lastname
        client.user.email=email
        client.nombre_de_voiture=nbr_voiture
        client.save()
        client.user.save()
        return redirect("show")  
    return render(request,'pfm/test/modifieclient.html', {'clients': client}) 
#----------------------------------------------------------------------------------------------------------------------------------------#
def destroy(request, id):  
    client =get_object_or_404(Client, user__id=id)  
    client.delete()  
    return redirect("show")
def confirm_delete(request, id):
    client = get_object_or_404(Client, user__id=id)
    return render(request, 'pfm/confirm_delete.html', {'client': client})

#-----------------------------------------------------------------------------------------------------------------------------------------#
def view(request,id):
    client = get_object_or_404(Client,user__id=id) 
    return render(request,"pfm/view.html",{'clients':client})
#-----------------------------------------------------------------------------------------------------------------------------------------#
#                                                                                                                                         #
#                                                          Partie employe                                                                 #
#                                                                                                                                         #
#-----------------------------------------------------------------------------------------------------------------------------------------#
def registerEmploye(request):
    if request.method == "POST":
        username = request.POST['username']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        password = request.POST['password']
        confirmpwd = request.POST['comfirmpwd']
        telphone = request.POST['telphone']
        dateembauche=request.POST['dateembauche']
        adress=request.POST['adress']
        role=request.POST['role']
        #--------------------------------------------------------partie filtre----------------------------------------------------------#
       
        if not username.isalnum():
            messages.error(request, "Le nom d'utilisateur n'est pas valide. Utilisez uniquement des lettres et des chiffres.")
            return redirect("registerEmploye")
        
        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, "L'adresse email n'est pas valide.")
            return redirect("registerEmploye")
        
        if not is_valid_name(firstname):
            messages.error(request, "Le prénom n'est pas valide. Utilisez uniquement des lettres.")
            return redirect("registerEmploye")
        
        if not is_valid_name(lastname):
            messages.error(request, "Le nom de famille n'est pas valide. Utilisez uniquement des lettres.")
            return redirect("registerEmploye")
        
        if not password_filter(password):
            messages.error(request, "mot de passe doit avoir 8 carctere, avoir majuscule miniscule nombre est des carctere ")
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "Le nom d'utilis sateur existe déjà.")
            return redirect("registerEmploye")
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "L'adresse email existe déjà.")
            return redirect("registerEmploye")
        
        if password != confirmpwd:
            messages.error(request, 'Le mot de passe ne correspondait pas ! ')  
            return redirect('registerEmploye')   
        if not is_integer(telphone):
            messages.error(request, "Le nombre de telphone doit être des nombre entier.")
            return redirect("registerEmploye")
        
            
        #-------------------------------------------------------------------------------------------------------------------------------------#
             
        my_user = User.objects.create_user(username, email, password)
        my_user.first_name =firstname
        my_user.last_name = lastname
        my_user.save()
        employe = Employe(user=my_user,telphone=telphone,dateembauche=dateembauche,adress=adress,role=role)
        employe.save()
        messages.success(request, 'Your account has been successfully created.')
    return render(request, 'pfm/test/createemploye.html')

def editEmploye(request, id):  
    employe = get_object_or_404(Employe,user__id=id) 
    return render(request,'pfm/test/modifieemploye.html', {'employes':employe})  
#------------------------------------------------------------------------------------------------------------------------------------------#
def updateEmploye(request, id):  
    employe = get_object_or_404(Employe, user__id=id)
    if request.method == "POST":        
        username = request.POST['username']
        firstname = request.POST['first_name']
        lastname = request.POST['last_name']
        email = request.POST['email']
        telphone = request.POST['telphone']
        #--------------------------------------------------------partie filtre----------------------------------------------------------#
        if not username.isalnum():
            messages.error(request, "Le nom d'utilisateur n'est pas valide. Utilisez uniquement des lettres et des chiffres.")
            return redirect("showemploye")

        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, "L'adresse email n'est pas valide.")
            return redirect("showemploye")
        
        if not is_valid_name(firstname):
            messages.error(request, "Le prénom n'est pas valide. Utilisez uniquement des lettres.")
            return redirect("showemploye")
        
        if not is_valid_name(lastname):
            messages.error(request, "Le nom de famille n'est pas valide. Utilisez uniquement des lettres.")
            return redirect("showemploye")
        
        if not is_integer(telphone):
            messages.error(request, "Le nombre de telphone doit être des nombre entier.")
            return redirect("showemploye")
        
        if User.objects.exclude(id=employe.user.id).filter(username=username).exists() and username != employe.user.username:
            messages.error(request, "Le nom d'utilisateur existe déjà.")
            return redirect("showemploye")
        
        if User.objects.exclude(id=employe.user.id).filter(email=email).exists() and email != employe.user.email:
            messages.error(request, "L'adresse email existe déjà.")
            return redirect("showemploye")
#-----------------------------------------------------------------------------------------------------------------------------------#
        employe.user.username=username  
        employe.user.first_name=firstname
        employe.user.last_name=lastname
        employe.user.email=email
        employe.telphone=telphone
        employe.save()
        employe.user.save()
        return redirect("showemploye")  
    return render(request,'pfm/test/modifieemploye.html', {'employes': employe}) 
#------------------------------------------------------------------------------------------------------------------------------------------#
def destroyEmploye(request, id):  
    employe =get_object_or_404(Employe, user__id=id)  
    employe.delete()  
    return redirect("showemploye")
#------------------------------------------------------------------------------------------------------------------------------------------#
def changepassword(request):
    if request.method=='POST':
        username=request.POST['username']
        user = User.objects.get(username=username)
        password=request.POST['password']
        password1=request.POST['password1']
        if password1!=password:
            messages.error(request, 'Le mot de passe ne correspondait pas !')  
            return redirect('modifiemotdepasse') 
        user.set_password(password)
        user.save()
        return redirect('home')
#------------------------------------------------------------------------------------------------------------------------------------------#
def viewemploye(request,id):
    employe = get_object_or_404(Employe,user__id=id) 
    return render(request,"pfm/viewemploye.html",{'employes':employe})
#-------------------------------------------------------------------------------------------------------------------------------------------#
def showemploye(request):
    employe=Employe.objects.all()
    return render(request,"pfm/test/manageemploye.html",{'employes':employe})
#-------------------------------------------------------------------------------------------------------------------------------------------#
#-------------------------------------------------------------------------------------------------------------------------------------------#
#                                                                                                                                           #
#                                                          Partie Voiture                                                                   #
#                                                                                                                                           #
#-------------------------------------------------------------------------------------------------------------------------------------------# 
from django.contrib import messages

def registervoiture(request):
    if request.method == "POST":
        immatriculation = request.POST['immatriculation']
        modele = request.POST['modele']
        genre = request.POST['genre']
        puissance = request.POST['puissance']
        km = request.POST['km']
        gam = request.POST['gam']
        date_naiss = request.POST['date_naiss']

        # Ajoutez des vérifications similaires à la fonction registerEmploye
        if not immatriculation.isalnum():
            messages.error(request, "L'immatriculation n'est pas valide. Utilisez uniquement des lettres et des chiffres.")
            return redirect("registervechule")

        # Ajoutez d'autres vérifications au besoin...

        # Créez l'objet Vechule et sauvegardez-le dans la base de données
        vechule = Vechule(immatriculation=immatriculation, modele=modele, genre=genre, puissance=puissance, km=km, gam=gam, date_naiss=date_naiss)
        vechule.save()

        # Ajoutez un message de succès
        messages.success(request, 'La voiture a été ajoutée avec succès.')

    return render(request, 'pfm/test/ajoutervechule.html')

#-------------------------------------------------------------------------------------------------------------------------------------------#
def showvechule(request):
    vechule=Vechule.objects.all()
    return render(request,"",{'vechule':vechule})  
#-------------------------------------------------------------------------------------------------------------------------------------------#
def destroyvechule(request,id):  
    vechule =get_object_or_404(Vechule,id=id)  
    vechule.delete()  
    return redirect("/avaiblevechule")
#--------------------------------------------------------------------------------------------------------------------------------------------#
def viewvechule(request,id):
    vechule = get_object_or_404(Vechule,id=id) 
    return render(request,"pfm/test/lieviewvechule.html",{'vechule':vechule})
#--------------------------------------------------------------------------------------------------------------------------------------------#
def affectation(request,id):
    vechule =get_object_or_404(Vechule,id=id)  
    if request.method == 'POST':
        username = request.POST['username']
        livraison=request.POST['livraison']
        fin_liv=request.POST['fin_liv']
        client = Client.objects.get(user__username=username)
        vechule.client = client
        vechule.livraison=livraison
        vechule.fin_liv=fin_liv
        vechule.save()
        return redirect('clientvechule')
    return render(request, 'pfm/test/lieviewvechule.html')
#-----------------------------------------------------------------------------------------------------------------------------------------#
#-----------------------------------------------------------------------------------------------------------------------------------------#
#-----------------------------------------------------------------------------------------------------------------------------------------#
#                                                                                                                                         #
#                                                         employe                                                                         #
#                                                                                                                                         #
#-----------------------------------------------------------------------------------------------------------------------------------------#
#-----------------------------------------------------------------------------------------------------------------------------------------#
#-----------------------------------------------------------------------------------------------------------------------------------------#
def remplcement(request, immatriculation):
    # Récupération du véhicule ayant l'immatriculation spécifiée.
    vechuleremp = Vechule.objects.get(immatriculation=immatriculation)

    # Récupération de la gamme ('gam') de ce véhicule.
    gam = vechuleremp.gam

    # Recherche de tous les véhicules qui appartiennent à la même gamme que le véhicule spécifié
    # et qui n'ont pas encore été attribués à un client (client__isnull=True).
    vechules = Vechule.objects.filter(client__isnull=True, gam=gam)

def dashboardemploye(request):
    return render(request,"pfm/test/dashboardemploye.html")

def clientvechule(request):
    vechules = Vechule.objects.exclude(client=None)
    return render(request, "pfm/test/clientvechule.html", {"vechules": vechules})
def avaiblevechule(request):
    vechules=Vechule.objects.filter(client=None)
    return render(request,"pfm/test/avaiblesvechule.html",{"vechules": vechules})


#-----------------------------------------------------------------------------------------------------------------------------------------#
#-----------------------------------------------------------------------------------------------------------------------------------------#
#                                                                                                                                         #
#                                                         Client                                                                          #
#                                                                                                                                         #
#-----------------------------------------------------------------------------------------------------------------------------------------#
#-----------------------------------------------------------------------------------------------------------------------------------------#
#-----------------------------------------------------------------------------------------------------------------------------------------#

def vechulefleet(request):
    client = Client.objects.get(user=request.user)
    vechule = Vechule.objects.filter(client=client)
    return render(request,"pfm/test/vechulefleet.html")

def vehicles_for_client(request):
    client = Client.objects.get(user=request.user)
    vechule = Vechule.objects.filter(client=client)
    return render(request, 'pfm/test/vechulefleet.html', {'vechules': vechule})

def remplacement(request, id):
    # Récupération du véhicule par son ID. Si non trouvé, une page 404 est retournée.
    vechule = get_object_or_404(Vechule, id=id)
    client = vechule.client

    # Vérifie si la requête est de type POST, ce qui indique la soumission d'un formulaire.
    if request.method == 'POST':
        # Récupération des données du formulaire.
        issuetype = request.POST.get('issuetype', '')
        date = request.POST.get('date', '')
        otherrequests = request.POST.get('otherrequests', '')
        dateincident = request.POST.get('dateincident', '')
        lieu_incident = request.POST.get('lieu_incident', '')
        Description = request.POST.get('Description', '')
        type_de_reparation = request.POST.get('type_de_reparation', '')

        # Gestion des champs de date pour s'assurer qu'ils ne sont pas vides.
        date = None if date == "" else date
        dateincident = None if dateincident == "" else dateincident

        # Assignation d'une valeur par défaut pour 'issuetype' si vide.
        issuetype = "other" if issuetype == "" else issuetype

        # Création d'un nouvel objet Remplacementvechule avec les données récupérées.
        remplace = Remplacementvechule(
            client=client,
            vechule=vechule,
            otherrequests=otherrequests,
            issuetype=issuetype,
            date=date,
            dateincident=dateincident,
            lieu_incident=lieu_incident,
            Description=Description,
            type_de_reparation=type_de_reparation
        )
        remplace.status = "Pending"  # Assignation du statut initial.
        remplace.save()  # Enregistrement de l'objet dans la base de données.

        # Redirection vers une autre page après la création de l'objet.
        return redirect('vechulefleet')

    # Si la requête n'est pas POST, la page du formulaire est affichée.
    return render(request, "pfm/test/viewClient.html", {'vechule': vechule})

def historique(request):
    # Récupère le client actuellement connecté.
    client = Client.objects.get(user=request.user)

    # Récupère tous les remplacements de véhicules associés à ce client.
    remplace = Remplacementvechule.objects.filter(client=client)

    # Rend le template 'historiqueclient.html' en passant les remplacements trouvés.
    return render(request, "pfm/test/historiqueclient.html", {'remplcements': remplace})

def remplacemnt_view(request, id):
    # Récupère un objet Remplacementvechule spécifique ou retourne une erreur 404 si non trouvé.
    remplacement = get_object_or_404(Remplacementvechule, id=id)

    # Met à jour le statut de l'objet Remplacementvechule.
    remplacement.status = "Processed"
    remplacement.save()

    # Assurez-vous que remplacement.vechule.date_naiss n'est pas None avant de procéder
    remplacement_date = remplacement.vechule.date_naiss

    if remplacement_date is not None:
        # Calcul des dates limites pour trouver des véhicules de remplacement
        date_limite_inf = remplacement_date - timedelta(days=3*365)
        date_limite_sup = remplacement_date + timedelta(days=3*365)
    else:
        # Utiliser la date actuelle comme valeurs par défaut pour les limites
        date_actuelle = datetime.now()
        date_limite_inf = date_actuelle - timedelta(days=3*365)
        date_limite_sup = date_actuelle + timedelta(days=3*365)

    # Récupère des véhicules disponibles pour le remplacement basé sur les dates calculées.
    vechules = Vechule.objects.filter(
        client=None,
        date_naiss__gte=date_limite_inf,
        date_naiss__lte=date_limite_sup
    )

    # Rend le template 'remplacementview.html' avec les données des véhicules disponibles et le remplacement en cours.
    return render(request, "pfm/test/remplacementview.html", {"vechules": vechules, "remplacement": remplacement}) 
def requestview(request):
    # Récupère les remplacements de véhicules qui n'ont pas encore d'historique.
    remplace = Remplacementvechule.objects.exclude(historique__isnull=False)

    # Rend le template 'newrequest.html' en passant les demandes de remplacement non traitées.
    return render(request, "pfm/test/newrequest.html", {'remplacements': remplace})

def remplacevechule(request, id, rempl_id):
    # Récupère le véhicule et la demande de remplacement spécifiques.
    vechule = get_object_or_404(Vechule, id=id)
    remplacement = get_object_or_404(Remplacementvechule, id=rempl_id)

    # Met à jour les informations du véhicule et de la demande de remplacement.
    vechule.client = remplacement.client
    remplacement.status = "Completed"
    remplacement.historique = "true"
    remplacement.vechule.cas = "virus"

    # Enregistre les modifications dans la base de données.
    remplacement.save()
    vechule.save()

    # Redirige vers la vue des demandes.
    return redirect("viewrequest")

def historique_request(request):
    # Récupère toutes les demandes de remplacement de véhicules.
    remplace = Remplacementvechule.objects.all()

    # Rend le template 'historiquerequest.html' avec toutes les demandes.
    return render(request, "pfm/test/historiquerequest.html", {"remplacements": remplace})
