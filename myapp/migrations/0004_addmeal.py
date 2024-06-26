# Generated by Django 4.2.9 on 2024-05-05 02:20

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("myapp", "0003_delete_recipe_instructions_model_alter_recipe_fat_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="AddMeal",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("MealName", models.CharField(max_length=255)),
                ("Calories", models.IntegerField()),
                ("Protein", models.IntegerField()),
                ("Fat", models.IntegerField()),
                ("Carbs", models.IntegerField()),
            ],
        ),
    ]
