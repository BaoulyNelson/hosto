
# Create your views here.
from .models import Patient,Medecin,Consultation,Prescription,Dossier,Departement,Commentaire
from .forms import PatientForm,MedecinForm,ConsultationForm,PrescriptionForm,DossierForm,CommentaireForm,DonForm
from django.contrib.auth.decorators import login_required
from .forms import DemandeConsultationForm,ProfileForm
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


def index(request):
    commentaires = Commentaire.objects.all()

    # Définir un content_type_id et object_id
    content_type_id = ContentType.objects.get_for_model(Commentaire).id
    commentaire_exemple = Commentaire.objects.first()
    object_id = commentaire_exemple.id if commentaire_exemple else None

    if request.user.is_authenticated:
        if request.user.is_superuser:
            return render(request, 'index.html', {'commentaires': commentaires})
        else:
            return render(request, 'accueil_utilisateur.html', {
                'commentaires': commentaires,
                'content_type_id': content_type_id,
                'object_id': object_id
            })
    else:
        return render(request, 'accueil_visiteur.html', {'commentaires': commentaires})

    
@login_required
def profile(request):
    return render(request, 'comptes/profile.html', {'user': request.user})



def login_view(request):
    # Supprime les anciens messages avant d'afficher un nouveau
    storage = get_messages(request)
    for _ in storage:
        pass  # Cette boucle vide supprime tous les anciens messages

    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, f"Bienvenue {username} ! 😊 Vous êtes connecté.")

                if request.POST.get("remember_me"):
                    request.session.set_expiry(1209600)  # 2 semaines

                return redirect("user_profile")
            else:
                messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
        else:
            messages.error(request, "Veuillez vérifier vos informations.")
    else:
        form = AuthenticationForm()

    return render(request, "comptes/login.html", {"form": form})


def signup_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Inscription réussie ! 🎉 Bienvenue sur notre plateforme.")
            return redirect("index")  # Redirection après succès
        else:
            messages.error(request, "Une erreur est survenue lors de l'inscription. Vérifiez les informations.")
    else:
        form = UserCreationForm()

    return render(request, "comptes/signup.html", {"form": form})




@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('index')  # Redirige vers la page d'accueil ou une autre page après la mise à jour
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
            form.save()
            return redirect(reverse(f"{type_entite}s_list"))  # Redirection dynamique
    else:
        form = FormClass()

    return render(request, 'ajouter_entite.html', {'form': form, 'type_entite': type_entite})



@login_required
def modifier_entite(request, type_entite, entite_id):
    # Mapping des modèles et formulaires
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

    # Récupération de l'entité
    entite = get_object_or_404(ModelClass, id=entite_id)

    if request.method == "POST":
        form = FormClass(request.POST, instance=entite)
        if form.is_valid():
            form.save()
            return redirect(reverse(f"{type_entite}s_list"))  # Redirection dynamique
    else:
        form = FormClass(instance=entite)

    return render(request, 'modifier_entite.html', {'form': form, 'type_entite': type_entite})



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
        return redirect(reverse(url_name))  # Redirection après suppression

    return render(request, 'supprimer_entite.html', {'entite': entite, 'type_entite': type_entite, 'url_name': url_name})



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

    
    
def soumettre_demande(request):
    if request.method == 'POST':
        form = DemandeConsultationForm(request.POST)
        if form.is_valid():
            form.save()  # Sauvegarder la demande dans la base de données
            return redirect('merci')  # Rediriger vers une page de remerciement
    else:
        form = DemandeConsultationForm()
    
    return render(request, 'soumettre_demande.html', {'form': form})


def merci(request):
    return render(request, 'merci.html')


def departements(request):
    departements_list = Departement.objects.all()
    return render(request, 'departements.html', {'departements': departements_list})


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
            commentaire.utilisateur = request.user  # Assignation de l'utilisateur actuel
            commentaire.save()

            # Utiliser un dictionnaire de correspondance pour la redirection
            url_mapping = {
                'patient': 'patients_list',
                'medecin': 'medecins_list',
                'consultation': 'consultations_list',
                'prescription': 'prescriptions_list',
                'dossier': 'dossiers_list',
            }

            # Récupérer le nom d'URL correspondant au type d'entité
            url_name = url_mapping.get(content_type.model, 'home')  # 'home' comme fallback si inconnu

            return redirect(url_name)  # Redirection vers l'URL correcte après ajout

    else:
        form = CommentaireForm()

    return render(request, 'ajouter_commentaire.html', {
        'form': form,
        'instance': instance,
        'content_type': content_type,  # Ajout du content_type
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

        return redirect(url_name)  # Rediriger vers l'URL correcte après la suppression

    return render(request, 'confirmer_suppression_commentaire.html', {
        'commentaire': commentaire
    })

    
def faire_don(request):
    form = DonForm()
    return render(request, 'don.html', {'form': form})

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
    
    return render(request, 'detail_patient.html', {
        'patient': patient,
        'commentaires': commentaires,
        'patient_content_type': patient_content_type
    })


def recherche(request):
    query = request.GET.get('q')
    patients = []
    medecins = []
    consultations = []
    prescriptions = []
    dossiers = []
    
    if query:
        # Rechercher des patients par nom ou prénom
        patients = Patient.objects.filter(nom__icontains=query) | Patient.objects.filter(prenom__icontains=query)

        # Rechercher des médecins par nom, prénom ou spécialité
        medecins = Medecin.objects.filter(nom__icontains=query) | Medecin.objects.filter(prenom__icontains=query) | Medecin.objects.filter(specialite__icontains=query)

        # Rechercher des consultations par diagnostique
        consultations = Consultation.objects.filter(diagnostique__icontains=query)

        # Rechercher des prescriptions par ID de consultation ou prescription
        prescriptions = Prescription.objects.filter(idconsultation__id__icontains=query) | Prescription.objects.filter(prescription__icontains=query)

        # Rechercher des dossiers par ID de consultation ou code
        dossiers = Dossier.objects.filter(idconsultation__id__icontains=query) | Dossier.objects.filter(code__icontains=query)

    context = {
        'patients': patients,
        'medecins': medecins,
        'consultations': consultations,
        'prescriptions': prescriptions,
        'dossiers': dossiers,
        'query': query,
    }
    return render(request, 'recherche.html', context)
