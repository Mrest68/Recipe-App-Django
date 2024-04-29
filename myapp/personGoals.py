from . import forms

class personGoals:

    
    @staticmethod
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
    @staticmethod
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
    @staticmethod
    def cals_permeal(Total_cals):
      
      mealCals = Total_cals/3

      return round(mealCals)

       







      





        

