from django.db import models

# Define your models here

class Recipe(models.Model):
    RecipeName = models.CharField(max_length=255)
    recipeImage = models.CharField(max_length=400)
    HealthLabels = models.CharField(max_length=500)
    Calories = models.IntegerField()
    Carbs = models.IntegerField()
    Protein = models.IntegerField()
    Fat = models.IntegerField()
    RecipeLink = models.CharField(max_length=500)

    def __str__(self):
        return self.RecipeName

class AddMeal(models.Model):
    MealName = models.CharField(max_length=255)
    MealDescription = models.CharField(max_length=500, default=None)
    Calories = models.IntegerField()
    Protein = models.IntegerField()
    Fat = models.IntegerField()
    Carbs = models.IntegerField()

    def __str__(self):
        return self.MealName

