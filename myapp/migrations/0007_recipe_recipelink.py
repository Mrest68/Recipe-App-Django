# Generated by Django 4.2.9 on 2024-05-15 20:55

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("myapp", "0006_rename_calories_recipe_calories_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="recipe",
            name="RecipeLink",
            field=models.CharField(default="", max_length=500),
            preserve_default=False,
        ),
    ]