import csv
from django.core.management.base import BaseCommand
from gestionhopital.models import Departement

class Command(BaseCommand):
    help = 'Importe les départements depuis un fichier CSV'

    def handle(self, *args, **kwargs):
        with open('departements.csv', mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            for row in reader:
                # Crée un département avec les données du CSV
                Departement.objects.create(
                    nom=row['nom'],
                    description=row['description'],
                    
                )
                
        self.stdout.write(self.style.SUCCESS('Départements importés avec succès!'))
