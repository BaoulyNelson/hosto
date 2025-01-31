# Generated by Django 4.2.16 on 2024-10-05 00:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Consultation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('poids', models.FloatField()),
                ('hauteur', models.FloatField()),
                ('diagnostique', models.TextField()),
                ('date_consultation', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='DemandeConsultation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100)),
                ('prenom', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('telephone', models.CharField(max_length=20)),
                ('message', models.TextField()),
                ('date_soumission', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Departement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('services', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Medecin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=50)),
                ('prenom', models.CharField(max_length=50)),
                ('sexe', models.CharField(max_length=8)),
                ('tel', models.CharField(max_length=20)),
                ('adresse', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=50)),
                ('specialite', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=50)),
                ('prenom', models.CharField(max_length=50)),
                ('sexe', models.CharField(max_length=8)),
                ('tel', models.CharField(max_length=20)),
                ('adresse', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Prescription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prescription', models.TextField()),
                ('idconsultation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestionhopital.consultation')),
            ],
        ),
        migrations.CreateModel(
            name='Dossier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=50)),
                ('date_enregistrement', models.DateField()),
                ('idconsultation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestionhopital.consultation')),
            ],
        ),
        migrations.AddField(
            model_name='consultation',
            name='idmedecin',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestionhopital.medecin'),
        ),
        migrations.AddField(
            model_name='consultation',
            name='idpatient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestionhopital.patient'),
        ),
    ]
