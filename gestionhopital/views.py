
# Create your views here.
from django.shortcuts import render, redirect
from .models import Patient,Medecin,Consultation,Prescription,Dossier,Departement,Commentaire
from .forms import PatientForm,MedecinForm,ConsultationForm,PrescriptionForm,DossierForm,CommentaireForm
from django.contrib.auth.decorators import login_required
from .forms import DemandeConsultationForm,FormulaireCreationUtilisateur, FormulaireAuthentificationPersonnalise, FormulaireReinitialisationMotDePasse
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth import views as auth_views
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.contrib import messages
from .forms import FormulaireReinitialisationMotDePasse  # Assurez-vous que le formulaire est correctement importé
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import SetPasswordForm
from django.utils.http import urlsafe_base64_decode
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseBadRequest
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

    
def inscription(request):
    if request.method == 'POST':
        form = FormulaireCreationUtilisateur(request.POST)
        if form.is_valid():
            form.save()  # Enregistre le nouvel utilisateur
            return redirect('index')  # Redirige vers la page de connexion
    else:
        form = FormulaireCreationUtilisateur()
    
    return render(request, 'comptes/inscription.html', {'form': form})


def connexion(request):
    if request.method == 'POST':
        form = FormulaireAuthentificationPersonnalise(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            # Authentifier l'utilisateur avec le backend personnalisé
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(request.GET.get('next', 'index'))  # 'index' peut être votre page d'accueil
            else:
                form.add_error(None, 'Identifiants invalides.')
    else:
        form = FormulaireAuthentificationPersonnalise()
    
    return render(request, 'comptes/connexion.html', {'form': form})



def deconnexion(request):
    if request.method == 'POST':
        # Si l'utilisateur confirme la déconnexion
        logout(request)
        return redirect('index')  # Rediriger vers la page d'accueil après la déconnexion
    return render(request, 'comptes/deconnexion.html')


def reinitialisation_mot_de_passe(request):
    if request.method == 'POST':
        form = FormulaireReinitialisationMotDePasse(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                messages.error(request, "Cet email n'est pas associé à un compte.")
                return render(request, 'comptes/reinitialisation_mot_de_passe.html', {'form': form})

            # Générez le token et l'UID
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)

            # Créez le lien de réinitialisation
            reset_link = request.build_absolute_uri(
                f'/reinitialisation_mot_de_passe_confirm/{uid}/{token}/'
            )

            # Envoyez un email à l'utilisateur avec le lien
            subject = "Réinitialisation de votre mot de passe"
            message = render_to_string('comptes/email_reinitialisation.html', {
                'user': user,
                'reset_link': reset_link,
            })
            send_mail(subject, message, 'no-reply@votresite.com', [email])

            messages.success(request, "Un email de réinitialisation a été envoyé à votre adresse.")
            return redirect('reinitialisation_mot_de_passe_effectuee')  # Redirigez vers une page de confirmation
    else:
        form = FormulaireReinitialisationMotDePasse()

    return render(request, 'comptes/reinitialisation_mot_de_passe.html', {'form': form})



def reinitialisation_mot_de_passe_confirm(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)  # Garder l'utilisateur connecté
                messages.success(request, "Votre mot de passe a été réinitialisé avec succès.")
                return redirect('connexion')
        else:
            form = SetPasswordForm(user)
        
        return render(request, 'comptes/reinitialisation_mot_de_passe_confirm.html', {'form': form})
    else:
        messages.error(request, "Le lien de réinitialisation est invalide.")
        return redirect('connexion')





@login_required
def ajouter_entite(request, type_entite):
    if request.method == "POST":
        if type_entite == 'patient':
            form = PatientForm(request.POST)
        elif type_entite == 'medecin':
            form = MedecinForm(request.POST)
        elif type_entite == 'consultation':
            form = ConsultationForm(request.POST)
        elif type_entite == 'prescription':
            form = PrescriptionForm(request.POST)
        elif type_entite == 'dossier':
            form = DossierForm(request.POST)
        else:
            form = None

        if form and form.is_valid():
            form.save()
            return redirect(reverse('liste_entites', args=[type_entite]))  # Dynamic redirection

    else:
        if type_entite == 'patient':
            form = PatientForm()
        elif type_entite == 'medecin':
            form = MedecinForm()
        elif type_entite == 'consultation':
            form = ConsultationForm()
        elif type_entite == 'prescription':
            form = PrescriptionForm()
        elif type_entite == 'dossier':
            form = DossierForm()
        else:
            form = None

    return render(request, 'ajouter_entite.html', {'form': form, 'type_entite': type_entite})




@login_required
def modifier_entite(request, type_entite, entite_id):
    # Récupérer l'entité correspondante à modifier en fonction du type
    if type_entite == 'patient':
        entite = get_object_or_404(Patient, id=entite_id)
        form = PatientForm(instance=entite)
    elif type_entite == 'medecin':
        entite = get_object_or_404(Medecin, id=entite_id)
        form = MedecinForm(instance=entite)
    elif type_entite == 'consultation':
        entite = get_object_or_404(Consultation, id=entite_id)
        form = ConsultationForm(instance=entite)
    elif type_entite == 'prescription':
        entite = get_object_or_404(Prescription, id=entite_id)
        form = PrescriptionForm(instance=entite)
    elif type_entite == 'dossier':
        entite = get_object_or_404(Dossier, id=entite_id)
        form = DossierForm(instance=entite)
    else:
        return HttpResponseBadRequest("Type d'entité inconnu")

    if request.method == "POST":
        if type_entite == 'patient':
            form = PatientForm(request.POST, instance=entite)
        elif type_entite == 'medecin':
            form = MedecinForm(request.POST, instance=entite)
        elif type_entite == 'consultation':
            form = ConsultationForm(request.POST, instance=entite)
        elif type_entite == 'prescription':
            form = PrescriptionForm(request.POST, instance=entite)
        elif type_entite == 'dossier':
            form = DossierForm(request.POST, instance=entite)
        
        if form.is_valid():
            form.save()
            return redirect(reverse('liste_entites', args=[type_entite]))

    return render(request, 'modifier_entite.html', {'form': form, 'type_entite': type_entite})


@login_required
def supprimer_entite(request, type_entite, entite_id):
    if type_entite == 'patient':
        entite = get_object_or_404(Patient, id=entite_id)
    elif type_entite == 'medecin':
        entite = get_object_or_404(Medecin, id=entite_id)
    elif type_entite == 'consultation':
        entite = get_object_or_404(Consultation, id=entite_id)
    elif type_entite == 'prescription':
        entite = get_object_or_404(Prescription, id=entite_id)
    elif type_entite == 'dossier':
        entite = get_object_or_404(Dossier, id=entite_id)
    else:
        return HttpResponseBadRequest("Type d'entité inconnu")

    if request.method == "POST":
        entite.delete()
        return redirect(reverse('liste_entites', args=[type_entite]))

    return render(request, 'supprimer_entite.html', {'entite': entite, 'type_entite': type_entite})



def liste_entites(request, type_entite):
    context = {}
    content_type = None  # Initialise content_type à None

    # Récupérer les entités en fonction du type
    if type_entite == 'patient':
        context['patients'] = Patient.objects.all()
        content_type = ContentType.objects.get_for_model(Patient)
    elif type_entite == 'medecin':
        context['medecins'] = Medecin.objects.all()
        content_type = ContentType.objects.get_for_model(Medecin)
    elif type_entite == 'consultation':
        context['consultations'] = Consultation.objects.all()
        content_type = ContentType.objects.get_for_model(Consultation)
    elif type_entite == 'prescription':
        context['prescriptions'] = Prescription.objects.all()
        content_type = ContentType.objects.get_for_model(Prescription)
    elif type_entite == 'dossier':
        context['dossiers'] = Dossier.objects.all()
        content_type = ContentType.objects.get_for_model(Dossier)
    else:
        # Si le type d'entité est invalide, vous pouvez renvoyer une 404 ou gérer l'erreur autrement
        return render(request, '404.html', status=404)

    # Récupérer les commentaires associés à chaque entité si le content_type a été défini
    if content_type:
        context['commentaires'] = Commentaire.objects.filter(content_type=content_type).order_by('-date_postee')



    # Passer le content_type au contexte pour l'utiliser dans le template
    context['content_type'] = content_type

    return render(request, 'liste_entites.html', context)
    
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

@login_required  # S'assurer que l'utilisateur est connecté
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
            
            # Assignation de l'utilisateur actuel
            commentaire.utilisateur = request.user  
            
            commentaire.save()
            return redirect('liste_entites', type_entite=content_type.model)  # Rediriger après ajout
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
        commentaire.delete()
        return redirect('liste_entites', type_entite=commentaire.content_type.model)

    return render(request, 'confirmer_suppression_commentaire.html', {
        'commentaire': commentaire
    })
    
    

@login_required
def admin_dashboard(request):
    total_utilisateurs = User.objects.count()
    total_commentaires = Commentaire.objects.count()
    total_departements = Departement.objects.count()
    total_medecins = Medecin.objects.count()
    total_patients = Patient.objects.count()
    total_prescriptions = Prescription.objects.count()  # Comptage des prescriptions
    total_dossiers = Dossier.objects.count()  # Comptage des dossiers

    context = {
        'total_utilisateurs': total_utilisateurs,
        'total_commentaires': total_commentaires,
        'total_departements': total_departements,
        'total_medecins': total_medecins,
        'total_patients': total_patients,
        'total_prescriptions': total_prescriptions,  # Ajout du total des prescriptions
        'total_dossiers': total_dossiers,  # Ajout du total des dossiers
    }
    return render(request, 'admin/admin_dashboard.html', context)

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
