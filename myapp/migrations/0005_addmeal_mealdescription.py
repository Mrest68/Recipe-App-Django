# Generated by Django 4.2.9 on 2024-05-05 21:11

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("myapp", "0004_addmeal"),
    ]

    operations = [
        migrations.AddField(
            model_name="addmeal",
            name="MealDescription",
            field=models.CharField(default=None, max_length=500),
        ),
    ]