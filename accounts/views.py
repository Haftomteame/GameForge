from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from games.models import Game, Favorite
from django.db.models import Q

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Compte créé pour {username}!')
            return redirect('accounts:login')
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def profile(request):
    query = request.GET.get('q', '')
    if query:
        user_games = Game.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(genre__icontains=query) |
            Q(ambiance__icontains=query) |
            Q(gameplay__icontains=query) |
            Q(story__icontains=query) |
            Q(characters__icontains=query) |
            Q(environment__icontains=query),
            user=request.user
        ).order_by('-created_at')
    else:
        user_games = Game.objects.filter(user=request.user).order_by('-created_at')

    # Récupérer les jeux favoris de l'utilisateur
    favorite_games = Game.objects.filter(favorite__user=request.user).order_by('-favorite__created_at')
    
    context = {
        'user_games': user_games,
        'favorite_games': favorite_games,
        'query': query
    }
    return render(request, 'accounts/profile.html', context)

@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Votre profil a été mis à jour avec succès!')
            return redirect('accounts:profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'accounts/edit_profile.html', context)

@login_required
def favorites(request):
    favorites = Favorite.objects.filter(user=request.user).select_related('game')
    return render(request, 'accounts/favorites.html', {'favorites': favorites})
