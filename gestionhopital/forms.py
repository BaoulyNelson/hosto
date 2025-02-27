from django import forms
from .models import Patient,Medecin,Consultation,Prescription,Dossier,DemandeConsultation,Commentaire
from datetime import date

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['nom', 'prenom', 'sexe', 'tel', 'adresse']

    # Champ sexe avec un select
    SEXE_CHOICES = [
        ('M', 'Masculin'),
        ('F', 'Féminin'),
        ('O', 'Autre'),
    ]
    
    sexe = forms.ChoiceField(choices=SEXE_CHOICES, label='Sexe')

    # Champ tel pour n'accepter que que les chiffres
    tel = forms.CharField(
        max_length=15,  # Ajustez selon la longueur de votre numéro
        label='Téléphone',
        widget=forms.NumberInput(attrs={
            'min': '0',  # Empêche la saisie de nombres négatifs
            'title': 'Entrez uniquement des chiffres.'
        })
    )


class MedecinForm(forms.ModelForm):
    class Meta:
        model = Medecin
        fields = ['nom', 'prenom', 'sexe', 'tel', 'adresse', 'email', 'specialite']

    # Champ sexe avec un select
    SEXE_CHOICES = [
        ('M', 'Masculin'),
        ('F', 'Féminin'),
        ('O', 'Autre'),
    ]
    
    sexe = forms.ChoiceField(choices=SEXE_CHOICES, label='Sexe')

    # Champ tel pour n'accepter que que les chiffres
    tel = forms.CharField(
        max_length=15,  # Ajustez selon la longueur de votre numéro
        label='Téléphone',
        widget=forms.NumberInput(attrs={
            'min': '0',  # Empêche la saisie de nombres négatifs
            'title': 'Entrez uniquement des chiffres.'
        })
    )



class ConsultationForm(forms.ModelForm):
    class Meta:
        model = Consultation
        fields = ['idmedecin', 'idpatient', 'poids', 'hauteur', 'diagnostique', 'date_consultation']

    # Utilisation d'un widget pour le champ de date avec un attribut max pour désactiver les dates futures
    date_consultation = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'max': date.today().strftime('%Y-%m-%d')  # Définit la date maximale au jour actuel
        }),
        label='Date de consultation'
    )


class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ['idconsultation', 'prescription']


class DossierForm(forms.ModelForm):
    class Meta:
        model = Dossier
        fields = ['code', 'idconsultation', 'date_enregistrement']

    # Utilisation du widget DateInput avec un attribut max pour empêcher la sélection de dates futures
    date_enregistrement = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'max': date.today().strftime('%Y-%m-%d')  # Définit la date maximale au jour actuel
        }),
        label='Date d\'enregistrement'
    )



class DemandeConsultationForm(forms.ModelForm):
    class Meta:
        model = DemandeConsultation
        fields = ['nom', 'prenom', 'email', 'telephone', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 5}),
        }
        
class FormulaireCreationUtilisateur(UserCreationForm):
    first_name = forms.CharField(
        required=True,
        label="Prénom",
        widget=forms.TextInput(attrs={'placeholder': 'Entrez votre prénom'})
    )
    last_name = forms.CharField(
        required=True,
        label="Nom",
        widget=forms.TextInput(attrs={'placeholder': 'Entrez votre nom'})
    )
    username = forms.CharField(
        required=True,
        label="Nom d’utilisateur",
        widget=forms.TextInput(attrs={'placeholder': 'Entrez votre nom d’utilisateur'})
    )
    
    email = forms.EmailField(
        required=True,
        label="Adresse email",
        widget=forms.EmailInput(attrs={'placeholder': 'Entrez votre adresse email'})
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')

    
    
   
class FormulaireAuthentificationPersonnalise(AuthenticationForm):
    username = forms.CharField(
        label="Nom d’utilisateur ou Email",
        widget=forms.TextInput(attrs={'placeholder': 'Entrez votre nom d’utilisateur ou email'})
    )
    password = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput(attrs={'placeholder': 'Entrez votre mot de passe'})
    )    
    

class FormulaireMiseAJourUtilisateur(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class FormulaireReinitialisationMotDePasse(PasswordResetForm):
    email = forms.EmailField(label="Adresse email")




class CommentaireForm(forms.ModelForm):
    class Meta:
        model = Commentaire
        fields = ['texte']
        
# Formulaire pour mettre à jour le profil de l'utilisateur
class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        from django import forms        


class DonForm(forms.Form):
    nom = forms.CharField(max_length=100)
    email = forms.EmailField()
    montant = forms.DecimalField(min_value=1, decimal_places=2)
    pays = CountryField().formfield(widget=CountrySelectWidget())
