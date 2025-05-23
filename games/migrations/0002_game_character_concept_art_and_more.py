# Generated by Django 5.2.1 on 2025-05-14 23:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='character_concept_art',
            field=models.ImageField(blank=True, null=True, upload_to='concept_art/characters/'),
        ),
        migrations.AddField(
            model_name='game',
            name='environment_concept_art',
            field=models.ImageField(blank=True, null=True, upload_to='concept_art/environments/'),
        ),
        migrations.AlterField(
            model_name='game',
            name='ambiance',
            field=models.CharField(choices=[('heroic', 'Héroïque'), ('dark', 'Sombre'), ('comedy', 'Comédie'), ('mystery', 'Mystère'), ('horror', 'Horreur'), ('fantasy', 'Fantaisie'), ('scifi', 'Science-Fiction'), ('realistic', 'Réaliste'), ('post_apo', 'Post-apocalyptique'), ('onirique', 'Onirique'), ('cyberpunk', 'Cyberpunk'), ('dark_fantasy', 'Dark Fantasy'), ('steampunk', 'Steampunk'), ('medieval', 'Médiéval')], max_length=20),
        ),
        migrations.AlterField(
            model_name='game',
            name='genre',
            field=models.CharField(choices=[('action', 'Action'), ('aventure', 'Aventure'), ('rpg', 'RPG'), ('strategie', 'Stratégie'), ('simulation', 'Simulation'), ('sport', 'Sport'), ('course', 'Course'), ('combat', 'Combat'), ('plateforme', 'Plateforme'), ('puzzle', 'Puzzle'), ('fps', 'FPS'), ('metroidvania', 'Metroidvania'), ('visual_novel', 'Visual Novel')], max_length=20),
        ),
    ]
