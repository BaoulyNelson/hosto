from django.contrib import admin
from .models import Patient, Medecin, Consultation, Prescription, Dossier, Commentaire, Departement,Contact,Actualite,Doctor
from .forms import DepartementForm



class DepartementAdmin(admin.ModelAdmin):
    form = DepartementForm
    list_display = ('nom', 'description')  # Affichage des départements dans la liste
    search_fields = ('nom', 'description')  # Recherche dans le nom et la description


class ActualiteAdmin(admin.ModelAdmin):
    list_display = ('titre', 'type', 'date_publication')  # Colonnes à afficher dans la liste des actualités
    list_filter = ('type', 'date_publication')  # Filtre par type et date
    search_fields = ('titre', 'contenu')  # Recherche par titre et contenu
    ordering = ('-date_publication',)  # Tri par date de publication décroissante



# Enregistrement des modèles dans l'interface d'administration
admin.site.register(Patient)
admin.site.register(Medecin)
admin.site.register(Consultation)
admin.site.register(Prescription)
admin.site.register(Dossier)
admin.site.register(Commentaire)
admin.site.register(Contact)
admin.site.register(Actualite, ActualiteAdmin)



@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):list_display = ('name', 'speciality')
# Personnalisation du modèle Departement
admin.site.register(Departement, DepartementAdmin)
