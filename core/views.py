from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import GameGenerationForm
from games.models import Game
from .services import AIGameGenerator
import traceback

def home(request):
    public_games = Game.objects.filter(is_public=True).order_by('-created_at')[:6]
    return render(request, 'core/home.html', {'public_games': public_games})

@login_required
def explore(request):
    public_games = Game.objects.filter(is_public=True).order_by('-created_at')
    return render(request, 'core/explore.html', {'games': public_games})

@login_required
def generate_game(request):
    generated_content = None
    form = GameGenerationForm()
    if request.method == 'POST':
        # Récupération manuelle des champs du formulaire personnalisé
        title = request.POST.get('title', '').strip()
        genre = request.POST.get('genre', '').strip()
        ambiance = request.POST.get('ambiance', '').strip()
        references = request.POST.get('references', '').strip()
        form_valid = all([title, genre, ambiance])
        if form_valid:
            try:
                ai_generator = AIGameGenerator()
                if not ai_generator._check_rate_limit(request.user):
                    messages.error(request, 'Vous avez atteint votre limite quotidienne de génération.', extra_tags='Limite quotidienne atteinte')
                else:
                    try:
                        generated_content = ai_generator.generate_game_content(
                            title=title,
                            genre=genre,
                            ambiance=ambiance,
                            references=references
                        )
                        print("Contenu généré:", generated_content)
                        # Création et sauvegarde du jeu
                        game = Game(
                            user=request.user,
                            title=title,
                            genre=genre,
                            ambiance=ambiance,
                            description=generated_content.get('description', ''),
                            gameplay=generated_content.get('gameplay', ''),
                            story=generated_content.get('story', ''),
                            characters=generated_content.get('characters', ''),
                            environment=generated_content.get('environment', '')
                        )
                        if 'character_image' in generated_content and generated_content['character_image']:
                            game.character_concept_art = generated_content['character_image']
                        if 'environment_image' in generated_content and generated_content['environment_image']:
                            game.environment_concept_art = generated_content['environment_image']
                        game.save()
                        messages.success(request, 'Concept généré avec succès !')
                        # Rediriger vers la page de détail du jeu créé
                        return redirect('games:game_detail', game.id)
                    except Exception as e:
                        error_message = f"Erreur lors de la génération du contenu : {str(e)}"
                        print(error_message)
                        print(traceback.format_exc())
                        if "StopIteration" in str(e):
                            messages.error(
                                request, 
                                "Erreur de connexion à l'API Hugging Face. Le service est temporairement indisponible.",
                                extra_tags=f"Erreur API: Impossible de se connecter au service de génération de texte. Veuillez réessayer dans quelques minutes."
                            )
                        elif "API key" in str(e).lower():
                            messages.error(
                                request, 
                                "Erreur d'authentification avec l'API Hugging Face. Veuillez vérifier la configuration.",
                                extra_tags=f"Erreur API: {str(e)}"
                            )
                        elif "timeout" in str(e).lower():
                            messages.error(
                                request, 
                                "Le temps de génération a dépassé la limite. Veuillez réessayer.",
                                extra_tags=f"Timeout: {str(e)}"
                            )
                        elif "rate limit" in str(e).lower():
                            messages.error(
                                request, 
                                "Limite de requêtes API atteinte. Veuillez réessayer plus tard.",
                                extra_tags=f"Rate limit: {str(e)}"
                            )
                        else:
                            messages.error(
                                request, 
                                f"Une erreur est survenue lors de la génération : {str(e)}",
                                extra_tags=f"Erreur technique: {traceback.format_exc()}"
                            )
            except Exception as e:
                error_message = f"Erreur inattendue : {str(e)}"
                print(error_message)
                print(traceback.format_exc())
                messages.error(
                    request, 
                    error_message,
                    extra_tags=f"Erreur système: {traceback.format_exc()}"
                )
        else:
            messages.error(
                request, 
                "Veuillez remplir tous les champs obligatoires.",
                extra_tags="Champs manquants: " + ", ".join([f for f, v in [("Titre", title), ("Genre", genre), ("Thème", ambiance)] if not v])
            )
        context = {
            'title': title,
            'genre': genre,
            'ambiance': ambiance,
            'references': references,
            'generated_content': generated_content,
            'form': form,
        }
        print("Context envoyé au template:", context)
        return render(request, 'core/generate_game.html', context)
    else:
        return render(request, 'core/generate_game.html', {'form': form})

@login_required
def generate_random(request):
    try:
        # Vérification de la limite d'utilisation
        ai_generator = AIGameGenerator()
        if not ai_generator._check_rate_limit(request.user):
            messages.error(request, 'Vous avez atteint votre limite quotidienne de génération.')
            return redirect('core:generate_game')

        # Génération aléatoire
        try:
            generated_content = ai_generator.generate_random_game()
        except Exception as e:
            error_message = f"Erreur lors de la génération aléatoire : {str(e)}"
            print(error_message)
            print(traceback.format_exc())
            messages.error(request, error_message)
            return redirect('core:generate_game')

        # Création du jeu
        game = Game(
            user=request.user,
            title=generated_content.get('title', ''),
            genre=generated_content.get('genre', ''),
            ambiance=generated_content.get('ambiance', ''),
            description=generated_content.get('description', ''),
            gameplay=generated_content.get('gameplay', ''),
            story=generated_content.get('story', ''),
            characters=generated_content.get('characters', ''),
            environment=generated_content.get('environment', '')
        )

        # Sauvegarde des images générées
        try:
            if 'character_image' in generated_content and generated_content['character_image']:
                game.character_concept_art = generated_content['character_image']
            if 'environment_image' in generated_content and generated_content['environment_image']:
                game.environment_concept_art = generated_content['environment_image']
        except Exception as e:
            error_message = f"Erreur lors de la sauvegarde des images : {str(e)}"
            print(error_message)
            print(traceback.format_exc())
            messages.warning(request, "Le jeu a été créé mais il y a eu un problème avec les images.")

        try:
            game.save()
            messages.success(request, 'Un jeu aléatoire a été généré avec succès!')
            return redirect('games:game_detail', game.id)
        except Exception as e:
            error_message = f"Erreur lors de la sauvegarde du jeu : {str(e)}"
            print(error_message)
            print(traceback.format_exc())
            messages.error(request, error_message)
            return redirect('core:generate_game')

    except Exception as e:
        error_message = f"Erreur inattendue : {str(e)}"
        print(error_message)
        print(traceback.format_exc())
        messages.error(request, error_message)
        return redirect('core:generate_game')
