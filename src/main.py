import data
import ui
import datetime

def main():

    is_running = True
    while is_running:

        data.checkCsvFileExists()
        ui.showMainMenu()

        choice = ui.getIntInput("Enter your choice: ")
        if choice == 1:
            name = ui.getStringInput("Add Name of Nutrition Entry: ")
            protein = ui.getFloatInput("Add Protein in grams: ")
            fat = ui.getFloatInput("Add Fat in grams: ")
            carbs = ui.getFloatInput("Add Carbs in grams: ")
            calories = ui.getFloatInput("Add Calories in kcal: ")

            try:
                data.checkCsvFileExists()
                data.writeNutritionData((name, protein, fat, carbs, calories, datetime.datetime.now()))
                ui.addNutritionSuccessfull()
            except FileNotFoundError as e:
                data.createHeader()
                ui.addNutritionFailed(e)

        elif choice == 2:
            recipe = ui.getStringInput("Enter the name of the recipe to use from the Nutrition Entry List: ")
            entry = []
            try:
                entry = data.getEntryByName(recipe)

            except FileNotFoundError as e:
                data.createHeader()
                ui.addNutritionFailed(e)

            except ValueError as e:
                ui.addNutritionFailed(e)
                
            # Only proceed if entry was found
            if entry:
                try:
                    data.checkCsvFileExists()
                    data.writeNutritionData((entry[0]["Name"], entry[0]["Protein"], entry[0]["Fat"], entry[0]["Carbs"], entry[0]["Calories"], datetime.datetime.now()))
                    ui.addNutritionSuccessfull()
                except FileNotFoundError as e:
                    data.createHeader()
                    ui.addNutritionFailed(e)
            else:
                ui.addNutritionFailed("Recipe not found in the nutrition entry list.")

        elif choice == 3:
            try:
                entries = data.getAllEntries()
                ui.showEntries(entries)
            except FileNotFoundError as e:
                data.createHeader()
                ui.addNutritionFailed(e)
            except IndexError as e:
                ui.showEntriesFailed(e)

        elif choice == 5:
            is_running = False
            break

        else:
            ui.invalidChoice()

if __name__ == "__main__":
    main()
