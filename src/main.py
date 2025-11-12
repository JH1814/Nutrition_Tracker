import data
import ui
import datetime

running = True

def main():
 while running:
    ui.showMainMenu()
    choice = input("Enter your choice: ")
    if choice == "1":
        name = input("Add Name of Nutrition Entry")
        carbs = input("Add Carbs in grams")
        protein = input("Add Protein in grams")
        fats = input("Add Fats in grams")
        calories = input("Add Calories in kcal")
        date = datetime.datetime.now()

        try :
            data.writeNutritionData((name,  protein, fats, carbs, calories, date))
            ui.addNutritionSuccessfull()
        except FileNotFoundError as e:
            ui.addNutritionFailed(e)

    if choice == "2":
        recipe = input("Enter the name of the recipe to use from the Nutrition Entry List: ")
        entry = data.getEntryByName(recipe)

        try :
           data.writeNutritionData((entry[0]["Name"], entry[0]["Protein"], entry[0]["Fat"], entry[0]["Carbs"], entry[0]["Calories"], datetime.datetime.now()))
           ui.addNutritionSuccessfull()
        
        except FileNotFoundError as e:
           ui.addNutritionFailed(e)
           
    if choice == "3":
        entries = data.getAllEntries()
        ui.showEntries(entries)
       

# if choice =="5":
    #running = False
    #exit()





if __name__ == "__main__":
    main()
