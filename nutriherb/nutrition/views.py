from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import HerbOrFood, HealthIssue, Recipe, Favorite
from .serializers import HerbOrFoodSerializer, HealthIssueSerializer, RecipeSerializer, FavoriteSerializer


class HerbOrFoodViewSet(viewsets.ModelViewSet):
    queryset = HerbOrFood.objects.all()
    serializer_class = HerbOrFoodSerializer


class HealthIssueViewSet(viewsets.ModelViewSet):
    queryset = HealthIssue.objects.all()
    serializer_class = HealthIssueSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer


class FavoriteViewSet(viewsets.ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['post'])
    def toggle(self, request):
        recipe_id = request.data.get('recipe_id')
        if not recipe_id:
            return Response({'error': 'recipe_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        recipe = get_object_or_404(Recipe, id=recipe_id)
        fav, created = Favorite.objects.get_or_create(user=request.user, recipe=recipe)
        if not created:
            fav.delete()
            return Response({'status': 'removed'})
        return Response({'status': 'added'})


def recipe_detail_view(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    related_foods = recipe.herbs_or_foods.all()
    is_favorited = False
    if request.user.is_authenticated:
        is_favorited = Favorite.objects.filter(user=request.user, recipe=recipe).exists()
    return render(request, 'recipe_detail.html', {
        'recipe': recipe, 
        'related_foods': related_foods,
        'is_favorited': is_favorited
    })


def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect('home')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error}")
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def profile_view(request):
    favorites = Favorite.objects.filter(user=request.user).select_related('recipe')
    return render(request, 'profile.html', {'favorites': favorites})
