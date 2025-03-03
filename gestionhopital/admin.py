from django.contrib import admin
from .models import Patient, Medecin, Consultation, Prescription, Dossier, Commentaire

# Enregistrement des modèles dans l'interface d'administration
admin.site.register(Patient)
admin.site.register(Medecin)
admin.site.register(Consultation)
admin.site.register(Prescription)
admin.site.register(Dossier)
admin.site.register(Commentaire)
