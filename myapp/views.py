from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .forms import user_inputHome, AddMealsForm
from .apiRequest import api_Request
from .personGoals import personGoals
from .models import Recipe, AddMeal

def Landing_Page(request):
    if request.method == "POST":
        return render(request, 'home.html')
    return render(request, 'LandingPage.html')

def cals_permeal(Total_cals):
    mealCals = Total_cals / 3
    return round(mealCals)

def BMR(new_Height, new_Weight, Age, Gender):
    if Gender == "M":
        BMR = 88.362 + (13.397 * new_Weight) + (4.799 * new_Height) - (5.677 * Age)
    elif Gender == "F":
        BMR = 447.593 + (9.247 * new_Weight) + (3.098 * new_Height) - (4.330 * Age)
    return BMR

def convert_Metrics(Height, Weight):
    try:
        feet, inches = Height.split("'")
        feet = int(feet.strip())
        inches = int(inches.replace('"', '').strip())
        new_Height = (feet * 30.48) + (inches * 2.54)
    except ValueError:
        raise ValueError("Height must be entered in feet and inches format, like 5'11\".")
    new_Weight = Weight * 0.453592
    return new_Height, new_Weight

def UserInputForm(request):
    form = user_inputHome(request.POST or None)
    mealCals = 0
    if request.method == "POST":
        if form.is_valid():
            try:
                Weight = form.cleaned_data["Weight"]
                Height = form.cleaned_data["Height"]
                Age = form.cleaned_data["Age"]
                Gender = form.cleaned_data["Gender"]
                Activity_levels = form.cleaned_data["Actvity_levels"]
                Fitness_Goal = form.cleaned_data["Fitness_Goal"]
                Proteinperc = form.cleaned_data["Proteinperc"]
                Carbperc = form.cleaned_data["Carbperc"]
                Fatperc = form.cleaned_data["Fatperc"]
                MealType = form.cleaned_data["MealType"].lower()
                new_Height, new_Weight = convert_Metrics(Height, Weight)
                bmr = BMR(new_Height, new_Weight, Age, Gender)
                calc_Cals = personGoals.calc_calories(bmr, Activity_levels)
                new_bmr = calc_Cals
                calc_Goal, TargetCals = personGoals.Goal(new_bmr, Fitness_Goal)
                Total_cals = round(calc_Goal)
                calc_Calpermeal = personGoals.cals_permeal(Total_cals)
                mealCals = calc_Calpermeal
                request.session['TargetCals'] = TargetCals
                request.session['mealCals'] = mealCals
                request.session['Proteinperc'] = Proteinperc
                request.session['Carbperc'] = Carbperc
                request.session['Fatperc'] = Fatperc
                request.session['MealType'] = MealType
                
                return redirect(Recipe_Page)
            except ValueError as e:
                form.add_error(None, str(e))
        else:
            return render(request, 'home.html', {'form': form})
    return render(request, 'home.html', {'form': form})

def Recipe_Page(request):
    mealCals = request.session.get('mealCals', 0)
    Proteinperc = request.session.get('Proteinperc', 0)
    Carbperc = request.session.get('Carbperc', 0)
    Fatperc = request.session.get('Fatperc', 0)
    MealType = request.session.get('MealType')
    
    apiCall = api_Request()
    response1 = apiCall.main(mealCals, Proteinperc, Fatperc, Carbperc, MealType)
    maxCals = round(request.session.get('TargetCals', 0))
    TargetProtein = round((maxCals * (request.session.get('Proteinperc', 0) / 100)) / 4)
    TargetCarbs = round((maxCals * (request.session.get('Carbperc', 0) / 100)) / 4)
    TargetFat = round((maxCals * (request.session.get('Fatperc', 0) / 100)) / 9)

    form = AddMealsForm()
    meals = AddMeal.objects.all()

    context = {
        'recipes_data': response1,
        'form': form,
        'meals': meals,
        'MaxCals': maxCals,
        'TargetProtein': TargetProtein,
        'TargetCarbs': TargetCarbs,
        'TargetFat': TargetFat
    }

    return render(request, 'recipes.html', context)

def add_meal(request):
    if request.method == 'POST':
        form = AddMealsForm(request.POST)
        if form.is_valid():
            meal = form.save()
            max_cals = request.session.get('TargetCals', 0)
            new_max_cals = max_cals - meal.Calories

            target_protein = request.session.get('TargetProtein', 0)
            new_target_protein = target_protein - meal.Protein

            target_carbs = request.session.get('TargetCarbs', 0)
            new_target_carbs = target_carbs - meal.Carbs

            target_fat = request.session.get('TargetFat', 0)
            new_target_fat = target_fat - meal.Fat

            request.session['TargetCals'] = new_max_cals
            request.session['TargetProtein'] = new_target_protein
            request.session['TargetCarbs'] = new_target_carbs
            request.session['TargetFat'] = new_target_fat

            response_data = {
                'id': meal.id,
                'name': meal.MealName,
                'description': meal.MealDescription,
                'calories': meal.Calories,
                'protein': meal.Protein,
                'fat': meal.Fat,
                'carbs': meal.Carbs,
                'max_cals': new_max_cals,
                'target_protein': new_target_protein,
                'target_carbs': new_target_carbs,
                'target_fat': new_target_fat,
            }
            return JsonResponse(response_data, status=201)
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

def delete_meal(request, meal_id):
    if request.method == 'POST':
        try:
            meal = AddMeal.objects.get(id=meal_id)
            meal_calories = meal.Calories
            meal_protein = meal.Protein
            meal_carbs = meal.Carbs
            meal_fat = meal.Fat

            meal.delete()
            max_cals = request.session.get('TargetCals', 0)
            new_max_cals = max_cals + meal_calories

            target_protein = request.session.get('TargetProtein', 0)
            new_target_protein = target_protein + meal_protein

            target_carbs = request.session.get('TargetCarbs', 0)
            new_target_carbs = target_carbs + meal_carbs

            target_fat = request.session.get('TargetFat', 0)
            new_target_fat = target_fat + meal_fat

            request.session['TargetCals'] = new_max_cals
            request.session['TargetProtein'] = new_target_protein
            request.session['TargetCarbs'] = new_target_carbs
            request.session['TargetFat'] = new_target_fat

            return JsonResponse({
                'status': 'success',
                'message': 'Meal deleted successfully',
                'max_cals': new_max_cals,
                'target_protein': new_target_protein,
                'target_carbs': new_target_carbs,
                'target_fat': new_target_fat
            })
        except AddMeal.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Meal not found'}, status=404)
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

def MoreRecipes(request):
    return render(request, 'MoreRecipes.html')
