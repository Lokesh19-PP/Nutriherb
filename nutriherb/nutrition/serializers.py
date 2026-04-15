from rest_framework import serializers
from .models import HerbOrFood, HealthIssue, Recipe, Favorite

class HerbOrFoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = HerbOrFood
        fields = ['id', 'name', 'category', 'nutrients', 'benefits']


class HealthIssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthIssue
        fields = ['id', 'name', 'description', 'herbs_or_foods']


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ['id', 'title', 'ingredients', 'steps', 'herbs_or_foods']


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ['id', 'user', 'recipe', 'created_at']
        read_only_fields = ['user']
