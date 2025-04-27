from django.urls import path
from .views import index,recherche_globale,ajouter_entite,modifier_entite,supprimer_entite,departements,ajouter_commentaire,supprimer_commentaire,merci,faire_don,process_don
# Importation des vues de Django pour la gestion de l'authentification
from . import views

from django.contrib.auth import views as auth_views
urlpatterns = [
    path('', index, name='index'),
 # Ajoute cette ligne dans ton `urls.py`
    path('signup/', views.signup_view, name='signup'),
    # Page de connexion
    path('login/', views.login_view, name='login'),
    
    # Page de déconnexion
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('confirmer-deconnexion/', views.confirmer_deconnexion, name='confirmer_deconnexion'),

    # Exemple de route pour le profil de l'utilisateur
    path('profile/', views.profile, name='profile'),
    path('apropos/', views.apropos, name='apropos'),

    # Changer de mot de passe
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),

    # Réinitialisation de mot de passe
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='comptes/password_reset_form.html'
    ), name='password_reset'),

    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='comptes/password_reset_done.html'
    ), name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='comptes/password_reset_confirm.html'
    ), name='password_reset_confirm'),

    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='comptes/password_reset_complete.html'
    ), name='password_reset_complete'),


    path('patients/', views.liste_entites_generique, {'type_entite': 'patient', 'template_name': 'patients/liste_patients.html'}, name='patients_list'),
    path('medecins/', views.liste_entites_generique, {'type_entite': 'medecin', 'template_name': 'medecins/liste_medecins.html'}, name='medecins_list'),
    path('consultations/', views.liste_entites_generique, {'type_entite': 'consultation', 'template_name': 'consultations/liste_consultations.html'}, name='consultations_list'),
    path('prescriptions/', views.liste_entites_generique, {'type_entite': 'prescription', 'template_name': 'prescriptions/liste_prescriptions.html'}, name='prescriptions_list'),
    path('dossiers/', views.liste_entites_generique, {'type_entite': 'dossier', 'template_name': 'dossiers/liste_dossiers.html'}, name='dossiers_list'),


    path('nos-medecins/', views.doctors_view, name='nos_medecins'),

    # URL pour éditer le profil utilisateur
    path('edit_profile/', views.edit_profile, name='edit_profile'),  # URL pour modifier le profil

    path('ajouter/<str:type_entite>/', ajouter_entite, name='ajouter_entite'),
    
    path('modifier/<str:type_entite>/<int:entite_id>/', modifier_entite, name='modifier_entite'),
    
    path('supprimer/<str:type_entite>/<int:entite_id>/', supprimer_entite, name='supprimer_entite'),

 
    path('merci/', merci, name='merci'),
    path('departements/', departements, name='departements'),
    
    path('ajouter_commentaire/<int:content_type_id>/<int:object_id>/', ajouter_commentaire, name='ajouter_commentaire'),
    path('faire_don/',faire_don, name='faire_don'),
    path('process_don/', process_don, name='process_don'),  # Ajoutez cette ligne

    path('supprimer_commentaire/<int:commentaire_id>/', supprimer_commentaire, name='supprimer_commentaire'),

    path('contact/', views.contact_view, name='contact'),
    path('contact/success/', views.contact_success_view, name='contact_success'),

    # ------------------- Recherche Globale -------------------
    path('recherche/', views.recherche_globale, name='recherche_globale'),
]
