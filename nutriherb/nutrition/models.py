from django.db import models
from django.contrib.auth.models import User

class HerbOrFood(models.Model):
    """Represents a specific nutrient-rich food or holistic herb."""
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    nutrients = models.TextField(blank=True)
    benefits = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Herbs & Foods"

    def __str__(self) -> str:
        return self.name


class HealthIssue(models.Model):
    """Represents a common health concern with supportive dietary recommendations."""
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    herbs_or_foods = models.ManyToManyField(
        'HerbOrFood', 
        related_name='health_issues', 
        blank=True
    )

    def __str__(self) -> str:
        return self.name


class Recipe(models.Model):
    """A culinary recipe utilizing one or more superfoods."""
    title = models.CharField(max_length=255)
    ingredients = models.TextField(blank=True)
    steps = models.TextField(blank=True)
    herbs_or_foods = models.ManyToManyField(
        'HerbOrFood', 
        related_name='recipes', 
        blank=True
    )

    def __str__(self) -> str:
        return self.title


class Favorite(models.Model):
    """Tracks which recipes a user has marked as high-priority favorites."""
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='favorites'
    )
    recipe = models.ForeignKey(
        'Recipe', 
        on_delete=models.CASCADE, 
        related_name='favorited_by'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'recipe')
        ordering = ['-created_at']

    def __str__(self) -> str:
        return f"{self.user.username} saved {self.recipe.title}"
