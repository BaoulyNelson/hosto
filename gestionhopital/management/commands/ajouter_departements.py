from django.core.management.base import BaseCommand
from gestionhopital.models import Departement

class Command(BaseCommand):
    help = 'Ajouter des départements prédéfinis'

    def handle(self, *args, **kwargs):
        departements_data = [
    {'nom': 'Cardiologie', 'description': 'Département de soins cardiaques', 'services': 'Consultation, Soins Intensifs'},
    {'nom': 'Neurologie', 'description': 'Département de neurologie', 'services': 'IRM, EEG'},
    {'nom': 'Orthopédie', 'description': 'Soins osseux et articulaires', 'services': 'Chirurgie, Rééducation'},
    {'nom': 'Pédiatrie', 'description': 'Soins pour enfants', 'services': 'Consultation, Vaccination'},
    {'nom': 'Dermatologie', 'description': 'Soins de la peau', 'services': 'Laser, Traitement des allergies'},
    {'nom': 'Oncologie', 'description': 'Traitement des cancers', 'services': 'Chimiothérapie, Radiothérapie'},
    {'nom': 'Gynécologie', 'description': 'Soins de la santé féminine', 'services': 'Consultation, Échographie'},
    {'nom': 'Ophtalmologie', 'description': 'Soins des yeux', 'services': 'Examen de la vue, Chirurgie au laser'},
    {'nom': 'ORL', 'description': 'Soins des oreilles, nez et gorge', 'services': 'Audiométrie, Chirurgie'},
    {'nom': 'Gastroentérologie', 'description': 'Soins digestifs', 'services': 'Endoscopie, Consultation'},
    {'nom': 'Urologie', 'description': 'Soins du système urinaire', 'services': 'Consultation, Chirurgie'},
    {'nom': 'Psychiatrie', 'description': 'Soins de santé mentale', 'services': 'Consultation, Thérapie'},
    {'nom': 'Pneumologie', 'description': 'Soins des poumons et voies respiratoires', 'services': 'Spirométrie, Bronchoscopie'},
    {'nom': 'Endocrinologie', 'description': 'Soins des glandes et des hormones', 'services': 'Consultation, Analyse sanguine'},
    {'nom': 'Néphrologie', 'description': 'Soins des reins', 'services': 'Dialyse, Consultation'},
    {'nom': 'Rhumatologie', 'description': 'Soins des maladies articulaires', 'services': 'Consultation, Thérapie'},
    {'nom': 'Infectiologie', 'description': 'Traitement des maladies infectieuses', 'services': 'Consultation, Antibiothérapie'},
    {'nom': 'Chirurgie générale', 'description': 'Interventions chirurgicales non spécialisées', 'services': 'Chirurgie, Soins post-opératoires'},
    {'nom': 'Radiologie', 'description': 'Imagerie médicale', 'services': 'Radiographie, IRM'},
    {'nom': 'Anesthésie', 'description': 'Gestion de la douleur et anesthésie', 'services': 'Anesthésie générale, Bloc nerveux'},
]

        for data in departements_data:
            Departement.objects.create(**data)

        self.stdout.write(self.style.SUCCESS('Départements ajoutés avec succès !'))
