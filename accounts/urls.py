from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(
        template_name='accounts/login.html',
        success_url=reverse_lazy('core:home')
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(
        next_page=reverse_lazy('accounts:login')
    ), name='logout'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('favorites/', views.favorites, name='favorites'),
] 