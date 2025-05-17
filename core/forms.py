from django import forms
from games.models import Game

class GameGenerationForm(forms.ModelForm):
    keywords = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Ex: boucle temporelle, vengeance, IA rebelle...',
            'class': 'form-control'
        })
    )
    references = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Ex: Zelda, Hollow Knight, Disco Elysium...',
            'class': 'form-control'
        })
    )

    class Meta:
        model = Game
        fields = ['title', 'genre', 'ambiance', 'description', 'gameplay', 'story', 'characters', 'environment', 'concept_art']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Titre de votre jeu'
            }),
            'genre': forms.Select(attrs={
                'class': 'form-select',
                'style': 'background:#414868; color:#fff; border:none; border-radius:12px;'
            }),
            'ambiance': forms.Select(attrs={
                'class': 'form-select',
                'style': 'background:#414868; color:#fff; border:none; border-radius:12px;'
            }),
            'description': forms.Textarea(attrs={
                'rows': 4,
                'class': 'form-control',
                'placeholder': 'Décrivez brièvement votre jeu...'
            }),
            'gameplay': forms.Textarea(attrs={
                'rows': 4,
                'class': 'form-control',
                'placeholder': 'Décrivez les mécaniques de jeu principales...'
            }),
            'story': forms.Textarea(attrs={
                'rows': 4,
                'class': 'form-control',
                'placeholder': 'Racontez l\'histoire de votre jeu...'
            }),
            'characters': forms.Textarea(attrs={
                'rows': 4,
                'class': 'form-control',
                'placeholder': 'Décrivez les personnages principaux...'
            }),
            'environment': forms.Textarea(attrs={
                'rows': 4,
                'class': 'form-control',
                'placeholder': 'Décrivez l\'univers et l\'environnement...'
            }),
            'concept_art': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
        }

class GameEditSimpleForm(forms.ModelForm):
    references = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Ex: Zelda, Hollow Knight, Disco Elysium...',
            'class': 'form-control'
        })
    )
    class Meta:
        model = Game
        fields = ['title', 'genre', 'ambiance']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Titre de votre jeu'
            }),
            'genre': forms.Select(attrs={'class': 'form-select'}),
            'ambiance': forms.Select(attrs={'class': 'form-select'}),
        } 