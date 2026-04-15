from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets
from .models import HerbOrFood, HealthIssue, Recipe
from .serializers import HerbOrFoodSerializer, HealthIssueSerializer, RecipeSerializer


class HerbOrFoodViewSet(viewsets.ModelViewSet):
    queryset = HerbOrFood.objects.all()
    serializer_class = HerbOrFoodSerializer


class HealthIssueViewSet(viewsets.ModelViewSet):
    queryset = HealthIssue.objects.all()
    serializer_class = HealthIssueSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer


def recipe_detail_view(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    related_foods = recipe.herbs_or_foods.all()
    return render(request, 'recipe_detail.html', {'recipe': recipe, 'related_foods': related_foods})
