from django import forms


class user_inputHome(forms.Form):

    GenderChoices = [("M" , "Male") , ("F", "Female")]
    Fitness_GoalChoices = [("Bulking", "Bulking"), ("Cutting", "Cutting"), ("Maintaining", "Maintaining")]
    Fitness_level = [("low", "1-2 times a week"), ("average", "3-4 times a week"), ("high", "5-7 times a week")]

    Weight = forms.IntegerField(label= "Please Enter Weight: ", required=False)
    Height = forms.CharField(label = "Please Enter Height: ", required= False)
    Gender = forms.ChoiceField(choices = GenderChoices, label = "Please Enter Gender: " , required= False)
    Age = forms.IntegerField(label= "Please Enter Age: ", required= False)
    Actvity_levels = forms.ChoiceField(choices= Fitness_level, label = "How often do you exercise in a week? ", required= False)
    Fitness_Goal = forms.ChoiceField (choices = Fitness_GoalChoices, label = "Please Enter Fitness Goal: ", required= False)
    Proteinperc = forms.IntegerField(label= " Please enter your daily protein intake percentage goal: ", required= True)
    Carbperc = forms.IntegerField(label= " Please enter your daily protein intake percentage goal: ", required= True)
    Fatperc = forms.IntegerField(label= " Please enter your daily protein intake percentage goal: ", required= True)

# class FilterForm(forms.Forms):

#     MealTypeChoices = [("Breakfast", "Breakfast") , ("Lunch","Lunch"),( "Dinner","Dinner")]
#     MealType = forms.ChoiceField(choices = MealTypeChoices, label="Meal Type:", required=False)
