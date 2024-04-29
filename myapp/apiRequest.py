import requests
from .models import Recipe

apiKey = "103231bdc9cb46128b291faf018846b3"

class api_Request:
        

    def main(self, mealCals, Proteinperc, Fatperc, Carbperc):
        

        URL = "https://api.spoonacular.com/recipes/complexSearch?apiKey="
        min_cals = mealCals - 200
        max_cals = mealCals + 100
       
        minProtein = (float(mealCals) * float(Proteinperc)/100 ) /4
        minCarb = (float(mealCals) * float(Carbperc)/100) / 4
        minFat = (float(mealCals) * float(Fatperc) / 100) / 9 
       

       
        try:
              response = requests.get(f"{URL}{apiKey}&minCalories={min_cals}&maxCalories={max_cals}&minProtein={minProtein}&minCarb={minCarb}&minFat={minFat}")
              print(minProtein,minCarb,minFat)
              response.raise_for_status()
              recipes_data = response.json()
        
        except requests.RequestException as e:
        
            print(f"Error during API call {e}")
            return []
       

        data_json = self.decipher_json(recipes_data) #recipes_data
        return data_json
    
    # Deciphers the json returned from the apiRequest to Spooncular to display the options for the USER
    def decipher_json(self, recipes_data):
       
        recipes_list = recipes_data.get('results', [])
        data_json = []

        for data in recipes_list:
            nutrients_list = data.get('nutrition' , {}).get('nutrients', [])
            nutrients = {nutrient['name']: nutrient['amount'] for nutrient in nutrients_list}
            


            recipe = Recipe(

                title = data.get("title"),
                image = data.get("image"),
                calories = round(nutrients.get("Calories")),
                protein = round(nutrients.get("Protein")),
                fat = round(nutrients.get("Fat")),
                id = data.get("id")

            )
           

            data_json.append(recipe)

        Recipe.objects.bulk_create(data_json, ignore_conflicts=True)

        return data_json
    
    
       
    #Calls Spooncular with a request to return the recipe instructions of the recipe selected by the user
    def Recipe_Instructions(self, id, apiKey): #id, apiKey
        
        Recipe_Instructions_URL = (f"https://api.spoonacular.com/recipes/{id}/analyzedInstructions?apiKey={apiKey}")


        try:
            Recipe_response = requests.get(Recipe_Instructions_URL)
            Recipe_json = Recipe_response.json()
        except requests.exceptions as e:
            print(f"There was an error retrieving the Recipe Instructions {e}")

        Deciphered_Recipe = self.decipher_json_RecipeInstructions(Recipe_json)
        return Deciphered_Recipe




    #Deciphers the json returned by the Spooncular with the Recipe Instructions
    def decipher_json_RecipeInstructions(self, Recipe_json):
        Recipe_data = []
        comments = ""
        seen_ingredients = set()

        for recipe in Recipe_json:
            for step in recipe['steps']:
                
                ingredients_list = step.get('ingredients', [])
                ingredients = []

                for ingredient in ingredients_list:
                    if ingredient['name'] not in seen_ingredients:
                        seen_ingredients.add(ingredient['name'])
                        ingredients.append ({
                        'name': ingredient['name'],
                        'image': ingredient.get('image', 'No image available')
                        } )

                equipment = ', '.join([equipment['name'] for equipment in step.get('equipment', [])])

                theStep = step['step']


                #isolate and assign the step and comments that may come with the steps
                if "Comments:" in theStep:
                    mainStep, comments = theStep.split('Comments:', 1) # the one represents "maxsplit()"" which is an argument for the max amount of times it should be split
                    theStep = mainStep.strip() # strip gets rid of any spaces or trailing characters which cleans up the text
                else:
                    theStep = step['step']

                if not equipment:
                    equipment = ""

                step_detail = {
                "number": step['number'],
                "step":theStep,
                "ingredients":ingredients, #', '.join([ingredient['name'] for ingredient in step.get('ingredients', [])]),
                "equipment": equipment,
                

            }
                Recipe_data.append(step_detail)

        print("these are the seen ingredients", seen_ingredients)
        return Recipe_data, comments.strip()










        


       

          


        
            


            
           