from django.http import HttpRequest
from django.shortcuts import render, redirect
from .forms import user_inputHome
from .apiRequest import api_Request
from django.urls import reverse
from .personGoals import personGoals
from .models import Recipe
from django.shortcuts import render, get_object_or_404


# Create your views here.

def cals_permeal(Total_cals):
      
      mealCals = Total_cals/3

      return round(mealCals)


def Goal(new_bmr, Fitness_Goal):
    Total_cals = 0

    if Fitness_Goal != None:

        if Fitness_Goal == "Cutting":
                Total_cals = new_bmr - 300
        elif Fitness_Goal == "Maintaining":
                Total_cals = new_bmr
        elif Fitness_Goal == "Bulking":
                Total_cals = new_bmr + 300
    
    return Total_cals
        
            

def calc_calories(bmr, Activity_levels):
    fitness = {"low": (1.2 * bmr), "average": (1.55 * bmr), "high": (1.9*bmr) }
    new_bmr = 0

    if Activity_levels != None:
        if Activity_levels == "low":
            new_bmr = fitness["low"]
        elif Activity_levels == "average":
                new_bmr = fitness["average"]
        elif Activity_levels == "high":
                new_bmr = fitness["high"]

      
    return new_bmr
            
      

def BMR(new_Height, new_Weight, Age, Gender):
        
        if Gender == "M":
              BMR = 88.362 + (13.397 * new_Weight) + (4.799* new_Height) - (5.677 * Age)
        elif Gender == "F":
              BMR = 447.593 + (9.247 * new_Weight) + (3.098 * new_Height) - (4.330 * Age)


        return BMR


def convert_Metrics(Height, Weight):
         
        feet, inches = map(int, Height.split("'"))
        new_Height = (feet * 30.48) + (inches * 2.54) 
        new_Weight = Weight * 0.453592

        return new_Height, new_Weight

def home(request):

    form = user_inputHome(request.POST or None )
    mealCals = 0
    if request.method == "POST":
        if form.is_valid():

            Weight = form.cleaned_data["Weight"]
            Height = form.cleaned_data["Height"]
            Age = form.cleaned_data["Age"]
            Gender = form.cleaned_data["Gender"]
            Activity_levels = form.cleaned_data["Actvity_levels"]
            Fitness_Goal = form.cleaned_data["Fitness_Goal"]
            Proteinperc = form.cleaned_data["Proteinperc"]
            Carbperc = form.cleaned_data["Carbperc"]
            Fatperc = form.cleaned_data["Fatperc"]

            new_Height, new_Weight = convert_Metrics(Height, Weight)
            bmr = BMR(new_Height, new_Weight, Age, Gender)



            calc_Cals = personGoals.calc_calories(bmr, Activity_levels)
            new_bmr = calc_Cals

            calc_Goal = personGoals.Goal(new_bmr, Fitness_Goal)
            Total_cals = round(calc_Goal)
            
            calc_Calpermeal = personGoals.cals_permeal(Total_cals)

            
            mealCals = calc_Calpermeal
            
            request.session['mealCals'] = mealCals
            request.session['Proteinperc'] = Proteinperc
            request.session['Carbperc'] = Carbperc
            request.session['Fatperc']= Fatperc

            return redirect(Recipe_Page)
        

    
    return render (request, 'home.html', {'form': form})



def Recipe_Page(request ):
      
      mealCals = request.session.get('mealCals', 0)
      Proteinperc = request.session.get('Proteinperc',default = 0)
      Carbperc = request.session.get('Carbperc',default = 0)
      Fatperc = request.session.get('Fatperc',default = 0)


      apiCall = api_Request()

      response1 = apiCall.main(mealCals,Proteinperc,Fatperc, Carbperc)
      
      
      
      return render(request, 'recipes.html', {'recipes_data': response1})

def view_recipes(request, id ):
      api_call = api_Request()
      apiKey = "103231bdc9cb46128b291faf018846b3"


      InstructionsCall,Comments = api_call.Recipe_Instructions(id, apiKey)
      Recipe_General = get_object_or_404(Recipe, pk=id)

      Recipe_General.protein = round(Recipe_General.protein)
      Recipe_General.fat = round(Recipe_General.fat)

      return render(request, 'Recipe-Instructions.html', {
            'recipe': Recipe_General,
            'instructions': InstructionsCall,
            'Comments': Comments})

# def furtherFilter(request, data_json):

#         query = request.GET.get("", '')

#         if query:
#             filtered = Recipe.objects.filter(title__icontains=query)
#         else:
#             filtered = Recipe.objects.none()

        
#         return render(request, 'recipes/search_results.html', {'recipes':filtered})
