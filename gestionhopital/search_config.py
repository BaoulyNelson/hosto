# search_config.py

search_config = {
    'Patient': {
        'nom': 'CharField(max_length=50)',
        'prenom': 'CharField(max_length=50)',
        'sexe': 'CharField(max_length=8)',
        'tel': 'CharField(max_length=20)',
        'adresse': 'CharField(max_length=100)',
    },
    'Medecin': {
        'nom': 'CharField(max_length=50)',
        'prenom': 'CharField(max_length=50)',
        'sexe': 'CharField(max_length=8)',
        'tel': 'CharField(max_length=20)',
        'adresse': 'CharField(max_length=100)',
        'email': 'CharField(max_length=50)',
        'specialite': 'CharField(max_length=50)',
    },
    'Consultation': {
        'idmedecin': 'ForeignKey(Medecin, on_delete=models.CASCADE)',
        'idpatient': 'ForeignKey(Patient, on_delete=models.CASCADE)',
        'poids': 'FloatField()',
        'hauteur': 'FloatField()',
        'diagnostique': 'TextField()',
        'date_consultation': 'DateField()',
    },
    'Prescription': {
        'idconsultation': 'ForeignKey(Consultation, on_delete=models.CASCADE)',
        'prescription': 'TextField()',
    },
    'Dossier': {
        'code': 'CharField(max_length=50, unique=True)',
        'idconsultation': 'ForeignKey(Consultation, on_delete=models.CASCADE)',
        'date_enregistrement': 'DateField()',
    },
    'DemandeConsultation': {
        'nom': 'CharField(max_length=100)',
        'prenom': 'CharField(max_length=100)',
        'email': 'EmailField()',
        'telephone': 'CharField(max_length=20)',
        'message': 'TextField()',
        'date_soumission': 'DateTimeField(auto_now_add=True)',
    },
    'Departement': {
        'nom': 'CharField(max_length=100)',
        'description': 'TextField()',
    },
    'Contact': {
        'type_demande': 'CharField(max_length=20, choices=TYPE_CHOICES)',
        'nom': 'CharField(max_length=100)',
        'prenom': 'CharField(max_length=100)',
        'email': 'EmailField()',
        'telephone': 'CharField(max_length=20, blank=True)',
        'sujet': 'CharField(max_length=150, blank=True)',
        'message': 'TextField()',
        'date_envoi': 'DateTimeField(auto_now_add=True)',
    },
    'Commentaire': {
        'utilisateur': 'ForeignKey(User, on_delete=models.CASCADE)',
        'texte': 'TextField()',
        'date_postee': 'DateTimeField(auto_now_add=True)',
        'content_type': 'ForeignKey(ContentType, on_delete=models.CASCADE)',
        'object_id': 'PositiveIntegerField()',
        'content_object': 'GenericForeignKey(content_type, object_id)',
    },
}

