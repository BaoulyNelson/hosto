from django.urls import path
from .views import index,inscription, connexion, reinitialisation_mot_de_passe,reinitialisation_mot_de_passe_confirm,deconnexion,recherche,ajouter_entite,modifier_entite,supprimer_entite,liste_entites,departements,ajouter_commentaire,supprimer_commentaire,soumettre_demande,merci

urlpatterns = [
    path('', index, name='index'),
    path('inscription/', inscription, name='inscription'),
    path('connexion/', connexion, name='connexion'),
 
    path('deconnexion/', deconnexion, name='deconnexion'),

    path('reinitialisation_mot_de_passe/', reinitialisation_mot_de_passe, name='reinitialisation_mot_de_passe'),
    
    path('reinitialisation_mot_de_passe_confirm/<uidb64>/<token>/',reinitialisation_mot_de_passe_confirm, name='reinitialisation_mot_de_passe_confirm'),
    
    path('ajouter/<str:type_entite>/', ajouter_entite, name='ajouter_entite'),
    
    path('modifier/<str:type_entite>/<int:entite_id>/', modifier_entite, name='modifier_entite'),
    
    path('supprimer/<str:type_entite>/<int:entite_id>/', supprimer_entite, name='supprimer_entite'),

    path('liste/<str:type_entite>/', liste_entites, name='liste_entites'),
    

 
    path('soumettre-demande/',soumettre_demande, name='soumettre_demande'),
    path('merci/', merci, name='merci'),
    path('departements/', departements, name='departements'),
    
    path('ajouter_commentaire/<int:content_type_id>/<int:object_id>/', ajouter_commentaire, name='ajouter_commentaire'),
    
    path('supprimer_commentaire/<int:commentaire_id>/', supprimer_commentaire, name='supprimer_commentaire'),


    path('recherche/', recherche, name='recherche'),  # Ajouter cette ligne
  

]
