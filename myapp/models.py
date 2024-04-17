from django.db import models

# Create your models here.

class Recipe(models.Model):
    title = models.CharField(max_length=255)
    image = models.CharField(max_length= 400)
    calories = models.IntegerField()
    protein = models.CharField(max_length=30)
    fat = models.CharField(max_length=30)
    carbs = models.CharField(max_length=30)


    def __str__(self):
        return self.title


