import data
import ui
import datetime

def main():

    is_running = True
    while is_running:
        ui.showMainMenu()
        choice = ui.getIntInput("Enter your choice: ")
        print(choice)
        if choice == 1:
            name = ui.getStrintInput("Add Name of Nutrition Entry: ")
            carbs = ui.getFloatInput("Add Carbs in grams: ")
            protein = ui.getFloatInput("Add Protein in grams: ")
            fats = ui.getFloatInput("Add Fats in grams: ")
            calories = ui.getFloatInput("Add Calories in kcal: ")

            try:
                data.writeNutritionData((name, protein, fats, carbs, calories, datetime.datetime.now()))
                ui.addNutritionSuccessfull()
            except FileNotFoundError as e:
              ui.addNutritionFailed(e)

        if choice == 2:
            recipe = input("Enter the name of the recipe to use from the Nutrition Entry List: ")
            entry = data.getEntryByName(recipe)

            try:
                data.writeNutritionData((entry[0]["Name"], entry[0]["Protein"], entry[0]["Fat"], entry[0]["Carbs"], entry[0]["Calories"], datetime.datetime.now()))
                ui.addNutritionSuccessfull()
            except FileNotFoundError as e:
                ui.addNutritionFailed(e)
           
        if choice == 3:
            entries = data.getAllEntries()
            ui.showEntries(entries)

        if choice == 5:
            is_running = False
            exit()

        else:
            ui.invalidChoice()

if __name__ == "__main__":
    main()
