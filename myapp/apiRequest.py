import requests
from .models import Recipe



class api_Request:
        

    def main(self, mealCals, Proteinperc, Fatperc, Carbperc):
       apiKey = "103231bdc9cb46128b291faf018846b3"

       URL = "https://api.spoonacular.com/recipes/complexSearch?apiKey="
       min_cals = mealCals - 200
       max_cals = mealCals + 100
       
       minProtein = (float(mealCals) * float(Proteinperc)/100 ) /4
       minCarb = (float(mealCals) * float(Carbperc)/100) / 4
       minFat = (float(mealCals) * float(Fatperc) / 100) / 9 
       

       
       try:
            response = requests.get(f"{URL}{apiKey}&minCalories={min_cals}&maxCalories={max_cals}&minProtein={minProtein}&minCarb={minCarb}&minFat={minFat}")
            response.raise_for_status()
            recipes_data = response.json()
       except requests.RequestException as e:
           print(f"Error during API call {e}")
           return []
       

       print(recipes_data,f"{URL}{apiKey}&minCalories={min_cals}&maxCalories={max_cals}")
       data_json = self.decipher_json(recipes_data)
       return data_json
    
    
    def decipher_json(self, recipes_data):

        # IDs = [int(recipe["id"]) for recipe in recipes_data]
        recipes_list = recipes_data.get('results', [])


        data_json = []

        for data in recipes_list:
            nutrients_info = recipes_data.get('nutrition', {}).get('nutrients',[])
            nutrients = {nutrient['name']: nutrient['amount'] for nutrient in nutrients_info}

            recipe = Recipe(

                title = data.get("title"),
                image = data.get("image"),
                calories = nutrients.get("calories"),
                protein = nutrients.get("protein"),
                fat = nutrients.get("fat"),
                carbs = nutrients.get("carbs")

            )
            data_json.append(recipe)

        Recipe.objects.bulk_create(data_json, ignore_conflicts=True)

        return data_json
       

    

        
            


            
           