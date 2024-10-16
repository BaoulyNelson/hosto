# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

class Patient(models.Model):
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    sexe = models.CharField(max_length=8)
    tel = models.CharField(max_length=20)
    adresse = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.nom} {self.prenom}'  # Affiche le nom complet du patient


class Medecin(models.Model):
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    sexe = models.CharField(max_length=8)
    tel = models.CharField(max_length=20)
    adresse = models.CharField(max_length=100)
    email = models.CharField(max_length=50)
    specialite = models.CharField(max_length=50)

    def __str__ (self):
        return f'Dr. {self.nom} {self.prenom}'  # Affiche le nom complet du médecin avec un titre


class Consultation(models.Model):
    idmedecin = models.ForeignKey(Medecin, on_delete=models.CASCADE)
    idpatient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    poids = models.FloatField()
    hauteur = models.FloatField()
    diagnostique = models.TextField()
    date_consultation = models.DateField()

    def __str__ (self):
        return f'{self.idmedecin} '  # Affiche l'id complet de la consultation 


class Prescription(models.Model):
    idconsultation = models.ForeignKey(Consultation, on_delete=models.CASCADE)
    prescription = models.TextField()
    
    

class Dossier(models.Model):
    code = models.CharField(max_length=50, unique=True)  # Le code est maintenant unique
    idconsultation = models.ForeignKey(Consultation, on_delete=models.CASCADE)
    date_enregistrement = models.DateField()



class DemandeConsultation(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField()
    telephone = models.CharField(max_length=20)
    message = models.TextField()
    date_soumission = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Demande de {self.nom} {self.prenom}"
    
    
class Departement(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField()
    services = models.TextField()

    def __str__(self):
        return self.nom
    
class Commentaire(models.Model):
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    texte = models.TextField()
    date_postee = models.DateTimeField(auto_now_add=True)

    # Champs pour les relations génériques
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return f'Commentaire de {self.utilisateur} sur {self.content_object}'