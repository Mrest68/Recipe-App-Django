# Generated by Django 4.2.9 on 2024-04-26 03:27

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("myapp", "0002_recipe_instructions_model_remove_recipe_carbs_and_more"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Recipe_Instructions_Model",
        ),
        migrations.AlterField(
            model_name="recipe",
            name="fat",
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name="recipe",
            name="protein",
            field=models.IntegerField(),
        ),
    ]
