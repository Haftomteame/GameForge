from django.db import models
from django.contrib.auth.models import User

class Game(models.Model):
    GENRE_CHOICES = [
        ('action', 'Action'),
        ('aventure', 'Aventure'),
        ('rpg', 'RPG'),
        ('strategie', 'Stratégie'),
        ('simulation', 'Simulation'),
        ('sport', 'Sport'),
        ('course', 'Course'),
        ('combat', 'Combat'),
        ('plateforme', 'Plateforme'),
        ('puzzle', 'Puzzle'),
        ('fps', 'FPS'),
        ('metroidvania', 'Metroidvania'),
        ('visual_novel', 'Visual Novel'),
    ]

    AMBIANCE_CHOICES = [
        ('heroic', 'Héroïque'),
        ('dark', 'Sombre'),
        ('comedy', 'Comédie'),
        ('mystery', 'Mystère'),
        ('horror', 'Horreur'),
        ('fantasy', 'Fantaisie'),
        ('scifi', 'Science-Fiction'),
        ('realistic', 'Réaliste'),
        ('post_apo', 'Post-apocalyptique'),
        ('onirique', 'Onirique'),
        ('cyberpunk', 'Cyberpunk'),
        ('dark_fantasy', 'Dark Fantasy'),
        ('steampunk', 'Steampunk'),
        ('medieval', 'Médiéval'),
    ]

    title = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    genre = models.CharField(max_length=20, choices=GENRE_CHOICES)
    ambiance = models.CharField(max_length=20, choices=AMBIANCE_CHOICES)
    description = models.TextField()
    gameplay = models.TextField()
    story = models.TextField()
    characters = models.TextField()
    environment = models.TextField()
    concept_art = models.ImageField(upload_to='concept_art/', null=True, blank=True)
    character_concept_art = models.ImageField(upload_to='concept_art/characters/', null=True, blank=True)
    environment_concept_art = models.ImageField(upload_to='concept_art/environments/', null=True, blank=True)
    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'game')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.game.title}"
