from django.urls import path
from .views import index,recherche,ajouter_entite,modifier_entite,supprimer_entite,liste_entites,departements,ajouter_commentaire,supprimer_commentaire,soumettre_demande,merci,faire_don,process_don
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
    # Exemple de route pour le profil de l'utilisateur
    path('accounts/profile/', views.profile, name='user_profile'),

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

     # URL pour éditer le profil utilisateur
    path('edit_profile/', views.edit_profile, name='edit_profile'),  # URL pour modifier le profil

    path('ajouter/<str:type_entite>/', ajouter_entite, name='ajouter_entite'),
    
    path('modifier/<str:type_entite>/<int:entite_id>/', modifier_entite, name='modifier_entite'),
    
    path('supprimer/<str:type_entite>/<int:entite_id>/', supprimer_entite, name='supprimer_entite'),

    path('liste/<str:type_entite>/', liste_entites, name='liste_entites'),
    

 
    path('soumettre-demande/',soumettre_demande, name='soumettre_demande'),
    path('merci/', merci, name='merci'),
    path('departements/', departements, name='departements'),
    
    path('ajouter_commentaire/<int:content_type_id>/<int:object_id>/', ajouter_commentaire, name='ajouter_commentaire'),
    path('faire_don/',faire_don, name='faire_don'),
    path('process_don/', process_don, name='process_don'),  # Ajoutez cette ligne

    path('supprimer_commentaire/<int:commentaire_id>/', supprimer_commentaire, name='supprimer_commentaire'),


    path('recherche/', recherche, name='recherche'),  # Ajouter cette ligne
  

]
