from django.db import models


class HerbOrFood(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    nutrients = models.TextField(blank=True)
    benefits = models.TextField(blank=True)

    def __str__(self) -> str:
        return self.name


class HealthIssue(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    herbs_or_foods = models.ManyToManyField(
        'HerbOrFood', related_name='health_issues', blank=True
    )

    def __str__(self) -> str:
        return self.name


class Recipe(models.Model):
    title = models.CharField(max_length=255)
    ingredients = models.TextField(blank=True)
    steps = models.TextField(blank=True)
    herbs_or_foods = models.ManyToManyField(
        'HerbOrFood', related_name='recipes', blank=True
    )

    def __str__(self) -> str:
        return self.title
