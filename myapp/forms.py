from django import forms
from .models import AddMeal

class user_inputHome(forms.Form):

    GenderChoices = [("M" , "Male") , ("F", "Female")]
    Fitness_GoalChoices = [("Bulking", "Bulking"), ("Cutting", "Cutting"), ("Maintaining", "Maintaining")]
    Fitness_level = [("low", "1-2 times a week"), ("average", "3-4 times a week"), ("high", "5-7 times a week")]
    MealType  = [("Breakfast", "Breakfast") , ("Lunch", "Lunch") , ("Dinner", "Dinner")]

    Weight = forms.IntegerField(label= "Please Enter Weight ", required=True)
    Height = forms.CharField(label = "Please Enter Height ", required= True)
    Gender = forms.ChoiceField(choices = GenderChoices, label = "Please Enter Gender " , required= True)
    Age = forms.IntegerField(label= "Please Enter Age ", required= False)
    Actvity_levels = forms.ChoiceField(choices= Fitness_level, label = "How often do you exercise in a week? ", required= False)
    Fitness_Goal = forms.ChoiceField (choices = Fitness_GoalChoices, label = "Please Enter Fitness Goal ", required= False)
    Proteinperc = forms.IntegerField(label= " Please enter your daily protein intake percentage goal ", required= False)
    Carbperc = forms.IntegerField(label= " Please enter your daily carbohydrate intake percentage goal ", required= False)
    Fatperc = forms.IntegerField(label= " Please enter your daily fat intake percentage goal", required= False)
    MealType = forms.ChoiceField(choices=MealType, label= "Please select meal type: ", required= False)

    def clean_weight(self):
        weight = self.cleaned_data.get('Weight')
       
        if not weight or weight > 350:
            raise forms.ValidationError("The entered weight seems unusually high. Please enter a valid weight.")
        return weight
    
    def clean_height(self):
        height = self.cleaned_data.get('Height')
        if not height or "'" not in height:
            raise forms.ValidationError("Please enter height in feet and inches format, like 5'11\".")
        parts = height.split("'")
        if len(parts) != 2:
            raise forms.ValidationError("Please enter a valid height.")
        try:
            feet = int(parts[0].strip())
            inches = int(parts[1].replace('"', '').strip())
        except ValueError:
            raise forms.ValidationError("Feet and inches must be whole numbers.")

        if not (0 <= feet <= 7 and 0 <= inches <= 11):  # Assuming a reasonable range for feet and inches
            raise forms.ValidationError("Height values are out of typical range.")
        return height

    def clean_age(self):
        age = self.cleaned_data('Age')
        if age > 100:
            raise forms.ValidationError("Please enter valid age")
        return age
        
class AddMealsForm(forms.ModelForm):
    MealName = forms.CharField(label = "Meal Name" , required=True)
    MealDescription = forms.CharField(label="Optional Meal Description", required=False)
    Calories = forms.IntegerField(label = "Calories Content" , required=True)
    Fat = forms.IntegerField(label = "Fat Content", required=False)
    Carbs = forms.IntegerField(label="Carbohydrate Content", required= False)
    Protein = forms.IntegerField(label="Protein Content", required= False)
    class Meta:
        model = AddMeal
        fields = ['MealName', 'MealDescription', 'Calories', 'Fat', 'Carbs', 'Protein']
        

# class FilterForm(forms.Forms):

#     MealTypeChoices = [("Breakfast", "Breakfast") , ("Lunch","Lunch"),( "Dinner","Dinner")]
#     MealType = forms.ChoiceField(choices = MealTypeChoices, label="Meal Type:", required=False)
