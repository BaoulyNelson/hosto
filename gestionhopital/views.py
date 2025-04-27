
# Create your views here.
from .models import Patient,Medecin,Consultation,Prescription,Dossier,Departement,Commentaire,Doctor,Actualite
from .forms import PatientForm,MedecinForm,ConsultationForm,PrescriptionForm,DossierForm,CommentaireForm,DonForm,ContactForm,ProfileForm
from django.contrib.auth.decorators import login_required

from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseBadRequest
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.messages import get_messages
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.http import Http404
from django.db.models import Q
from .search_config import search_config
from gestionhopital.utils import ajouter_message
from django.apps import apps
from django.contrib.auth import logout
from django.contrib.contenttypes.models import ContentType



    

def index(request):
    # Récupérer tous les commentaires
    commentaires = Commentaire.objects.all()

    # Récupérer les articles principaux (type='article')
    articles_principaux = Actualite.objects.filter(type='article')[:4]  # Par exemple, 2 articles principaux

    # Récupérer les événements et annonces (type='evenement' et 'annonce')
    evenements_et_annonces = Actualite.objects.filter(type__in=['evenement', 'annonce'])[:6]  # 4 événements/annonces

    # Définir content_type_id et object_id (pour le système de commentaires)
    content_type_id = ContentType.objects.get_for_model(Commentaire).id
    commentaire_exemple = Commentaire.objects.first()
    object_id = commentaire_exemple.id if commentaire_exemple else None

    # Rendu sur le template index.html avec les données mises à jour
    return render(request, 'index.html', {
        'commentaires': commentaires,
        'articles_principaux': articles_principaux,
        'evenements_et_annonces': evenements_et_annonces,
        'content_type_id': content_type_id,
        'object_id': object_id,
    })


    
@login_required
def profile(request):
    return render(request, 'comptes/profile.html', {'user': request.user})


def confirmer_deconnexion(request):
    if request.method == 'POST':
        logout(request)
        ajouter_message(request, 'success', "Vous avez été déconnecté avec succès.")
        return redirect('login')  # ou où tu veux après déconnexion
    return render(request, 'comptes/confirmer_deconnexion.html')


def login_view(request):
    if request.user.is_authenticated:
        ajouter_message(request, 'info', f"Vous êtes déjà connecté, {request.user.username}. 😊")
        return redirect('profile')

    storage = get_messages(request)
    for _ in storage:
        pass

    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                ajouter_message(request, 'success', f"Bienvenue {username} ! 😊 Vous êtes connecté.")

                if request.POST.get("remember_me"):
                    request.session.set_expiry(1209600)

                next_url = request.GET.get('next') or request.POST.get('next')
                if next_url:
                    return redirect(next_url)
                return redirect('profile')
            else:
                ajouter_message(request, 'error', "Nom d'utilisateur ou mot de passe incorrect.")
        else:
            ajouter_message(request, 'error', "Veuillez vérifier vos informations.")
    else:
        form = AuthenticationForm()

    return render(request, "comptes/login.html", {"form": form})




from django.shortcuts import render, redirect
from django.contrib.auth import login
from .utils import ajouter_message

def signup_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            ajouter_message(request, 'success', "Inscription réussie ! 🎉 Bienvenue sur notre plateforme.")
            return redirect("profile")  # Redirection après succès
        else:
            ajouter_message(request, 'error', "Une erreur est survenue lors de l'inscription. Vérifiez les informations.")
    else:
        form = UserCreationForm()

    return render(request, "comptes/signup.html", {"form": form})







@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            ajouter_message(request, 'success', "Votre profil a été mis à jour avec succès !")
            return redirect('profile')  # Redirige vers la page du profil après la mise à jour
    else:
        form = ProfileForm(instance=request.user)
    
    return render(request, 'comptes/edit_profile.html', {'form': form})






@login_required
def ajouter_entite(request, type_entite):
    form_mapping = {
        'patient': PatientForm,
        'medecin': MedecinForm,
        'consultation': ConsultationForm,
        'prescription': PrescriptionForm,
        'dossier': DossierForm,
    }

    if type_entite not in form_mapping:
        raise Http404("Type d'entité non trouvé")

    FormClass = form_mapping[type_entite]

    if request.method == "POST":
        form = FormClass(request.POST)
        if form.is_valid():
            entite = form.save()
            ajouter_message(request, 'success', f"{type_entite.capitalize()} ajouté avec succès ! ✅")
            return redirect(reverse(f"{type_entite}s_list"))  # Redirection dynamique
    else:
        form = FormClass()

    return render(request, 'entites/ajouter_entite.html', {'form': form, 'type_entite': type_entite})


@login_required
def modifier_entite(request, type_entite, entite_id):
    entite_mapping = {
        'patient': (Patient, PatientForm),
        'medecin': (Medecin, MedecinForm),
        'consultation': (Consultation, ConsultationForm),
        'prescription': (Prescription, PrescriptionForm),
        'dossier': (Dossier, DossierForm),
    }

    if type_entite not in entite_mapping:
        return HttpResponseBadRequest("Type d'entité inconnu")

    ModelClass, FormClass = entite_mapping[type_entite]

    entite = get_object_or_404(ModelClass, id=entite_id)

    if request.method == "POST":
        form = FormClass(request.POST, instance=entite)
        if form.is_valid():
            form.save()
            ajouter_message(request, 'success', f"{type_entite.capitalize()} modifié avec succès ! ✏️✅")
            return redirect(reverse(f"{type_entite}s_list"))
    else:
        form = FormClass(instance=entite)

    return render(request, 'entites/modifier_entite.html', {'form': form, 'type_entite': type_entite})



@login_required
def supprimer_entite(request, type_entite, entite_id):
    entite_mapping = {
        'patient': ('patients_list', Patient),
        'medecin': ('medecins_list', Medecin),
        'consultation': ('consultations_list', Consultation),
        'prescription': ('prescriptions_list', Prescription),
        'dossier': ('dossiers_list', Dossier),
    }

    if type_entite not in entite_mapping:
        return HttpResponseBadRequest("Type d'entité inconnu")

    url_name, ModelClass = entite_mapping[type_entite]
    entite = get_object_or_404(ModelClass, id=entite_id)

    if request.method == "POST":
        entite.delete()
        ajouter_message(request, 'success', f"{type_entite.capitalize()} supprimé avec succès ! ✅")
        return redirect(reverse(url_name))  # Redirection après suppression

    return render(request, 'entites/supprimer_entite.html', {
        'entite': entite, 
        'type_entite': type_entite,
        'url_name': url_name
    })



@login_required
def liste_entites_generique(request, type_entite, template_name):
    entites_mapping = {
        'patient': ('patients', Patient),
        'medecin': ('medecins', Medecin),
        'consultation': ('consultations', Consultation),
        'prescription': ('prescriptions', Prescription),
        'dossier': ('dossiers', Dossier),
    }

    if type_entite not in entites_mapping:
        raise Http404("Type d'entité non trouvé")

    key, model = entites_mapping[type_entite]
    context = {
        key: model.objects.all(),
        'content_type': ContentType.objects.get_for_model(model),
        'commentaires': Commentaire.objects.filter(
            content_type=ContentType.objects.get_for_model(model)
        ).order_by('-date_postee'),
    }

    return render(request, template_name, context)

    
def doctors_view(request):
    doctors = Doctor.objects.all()
    return render(request, 'medecins/medecins.html', {'doctors': doctors})


def merci(request):
    return render(request, 'merci/merci.html')


def departements(request):
    departements_list = Departement.objects.all()
    return render(request, 'departements/departements.html', {'departements': departements_list})



@login_required
def ajouter_commentaire(request, content_type_id, object_id):
    content_type = get_object_or_404(ContentType, id=content_type_id)
    model_class = content_type.model_class()
    instance = get_object_or_404(model_class, id=object_id)

    if request.method == 'POST':
        form = CommentaireForm(request.POST)
        if form.is_valid():
            commentaire = form.save(commit=False)
            commentaire.content_type = content_type
            commentaire.object_id = instance.id
            commentaire.utilisateur = request.user  # Assigner l'utilisateur actuel
            commentaire.save()

            # Ajout d'un message de succès
            ajouter_message(request, 'success', "Votre commentaire a été ajouté avec succès ! 📝✅")

            # Rediriger vers la page appropriée après ajout
            return redirect('index')  # Remplacer par l'URL appropriée après l'ajout

    else:
        form = CommentaireForm()

    return render(request, 'commentaires/ajouter_commentaire.html', {
        'form': form,
        'instance': instance,
        'content_type': content_type,
        'object_id': object_id,
    })

@login_required
def supprimer_commentaire(request, commentaire_id):
    commentaire = get_object_or_404(Commentaire, id=commentaire_id)

    # Vérifier si l'utilisateur est superuser
    if not request.user.is_superuser:
        return redirect('index')  # Rediriger vers la page d'index si l'utilisateur n'a pas les droits

    # Vérifier si la demande est un POST
    if request.method == 'POST':
        content_type = commentaire.content_type
        model_name = content_type.model

        # Dictionnaire de correspondance entre le modèle de contenu et l'URL à utiliser
        url_mapping = {
            'patient': 'patients_list',
            'medecin': 'medecins_list',
            'consultation': 'consultations_list',
            'prescription': 'prescriptions_list',
            'dossier': 'dossiers_list',
        }

        # Obtenir le nom de l'URL correspondant
        url_name = url_mapping.get(model_name, 'home')  # 'home' comme fallback si le modèle est inconnu

        commentaire.delete()

        # Ajout d'un message de succès après suppression
        ajouter_message(request, 'success', "Le commentaire a été supprimé avec succès. 🗑️✅")

        return redirect(url_name)  # Rediriger vers l'URL correcte après la suppression

    return render(request, 'commentaires/confirmer_suppression_commentaire.html', {
        'commentaire': commentaire
    })



@login_required
def faire_don(request):
    form = DonForm()
    return render(request, 'don/don.html', {'form': form})

def process_don(request):
    if request.method == 'POST':
        form = DonForm(request.POST)
        if form.is_valid():
            # Traitez les données du formulaire ici
            nom = form.cleaned_data['nom']
            email = form.cleaned_data['email']
            montant = form.cleaned_data['montant']
            pays = form.cleaned_data['pays']

            return HttpResponse(f"Merci {nom} pour votre don de {montant} € depuis {pays}!")

    return redirect('faire_don')



def detail_patient(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    commentaires = Commentaire.objects.filter(content_type=ContentType.objects.get_for_model(Patient), object_id=patient.id)
    patient_content_type = ContentType.objects.get_for_model(Patient)
    
    return render(request, 'patients/detail_patient.html', {
        'patient': patient,
        'commentaires': commentaires,
        'patient_content_type': patient_content_type
    })



def recherche_globale(request):
    query = request.GET.get('q', '')
    resultats = []

    if query:
        for nom_modele, champs in search_config.items():
            try:
                # Remplace 'inscriptions' par le nom de ton app
                modele = apps.get_model('gestionhopital', nom_modele)
                filtres = Q()
                for champ in champs:
                    filtres |= Q(**{f"{champ}__icontains": query})
                objets = modele.objects.filter(filtres)

                # Ajouter les objets au résultat global
                # Utilise extend pour ne pas créer une liste de listes
                resultats.extend(objets)
            except Exception as e:
                # Si un modèle ou un champ est invalide, on l'ignore
                print(f"Erreur avec {nom_modele}: {e}")
                continue

    return render(request, 'search/recherche.html', {
        'query': query,
        'resultats': resultats
    })




def contact_view(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()  # <-- ENREGISTRE EN BASE
            return render(request, "contact/contact_success.html")
    else:
        form = ContactForm()

    return render(request, "contact/contact.html", {"form": form})



def contact_success_view(request):
    return render(request, "contact/contact_success.html")

def apropos(request):
    return render(request, 'apropos/apropos.html')