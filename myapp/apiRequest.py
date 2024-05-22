import requests
from .models import Recipe


class api_Request:
   
        

    def main(self, mealCals, Proteinperc, Fatperc, Carbperc,MealType):
        

        URL = "https://api.edamam.com/api/recipes/v2?type=public&app_id=e4b6e46c&app_key=1c35e3fec76ac6871529fc903c94ca11"


        min_cals = mealCals - 200
        max_cals = mealCals + 100
       
        minProtein = round((float(mealCals) * float(Proteinperc)/100 ) /4)
        minCarb = round((float(mealCals) * float(Carbperc)/100) / 4)
        minFat = round((float(mealCals) * float(Fatperc) / 100) / 9 )

       
        try:

              url = f"{URL}&mealType={MealType}&calories={min_cals}-{max_cals}&nutrients[PROCNT]={minProtein}&nutrients[CHOCDF]={minCarb}&nutrients[FAT]={minFat}"
              response = requests.get(url)
              print(url)
              response.raise_for_status()
              recipes_data = response.json()
        
        except requests.RequestException as e:
        
            print(f"Error during API call {e}")
            return []
       

        data_json = self.decipher_json(recipes_data) #recipes_data
        return data_json
    
    # Deciphers the json returned from the apiRequest to Spooncular to display the options for the USER
    def decipher_json(self, recipes_data):
       
        hits = recipes_data.get('hits', [])
        recipeChecker = set()
        data_json = []

        for data in hits:
                recipe_info = data.get('recipe',{}).get('calories')
                if recipe_info not in recipeChecker:
                    recipeChecker.add(recipe_info)
                     
                    recipe_data = data.get('recipe', {})

                    recipeImage = recipe_data.get('image', '')
                
                    RecipeName = recipe_data.get('label', '')

                    HealthLabels = recipe_data.get('healthLabels', [])
                    Calories = recipe_data.get('calories', 0)
                    Digest = recipe_data.get('digest', [])
                    RecipeLink = recipe_data.get('url', '')

                    Fat = 0
                    Carbs = 0
                    Protein = 0
                    for nutrient in Digest:

                        if nutrient['label'] == 'Fat':
                            Fat = nutrient.get('total', 0)

                        if nutrient['label'] == 'Carbs':
                            Carbs = nutrient.get('total', 0)
                            
                        if nutrient['label'] == 'Protein':
                            Protein = nutrient.get('total', 0)
                    


                    recipe = Recipe(

                            RecipeName = RecipeName,
                            recipeImage = recipeImage,
                            Calories = round(Calories),
                            HealthLabels = HealthLabels,
                            Protein = round(Protein),
                            Fat = round(Fat),
                            Carbs = round(Carbs),
                            RecipeLink = RecipeLink
                        )

                
                    data_json.append(recipe)
                else:
                     continue

        Recipe.objects.bulk_create(data_json, ignore_conflicts=True)

        return data_json
    
    
       
  
  


   









        


       

          


        
            


            
           