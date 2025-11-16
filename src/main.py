import data
import ui
import datetime
import time

def main():

    is_running = True
    while is_running:

        data.checkCsvFileExists()
        ui.showMainMenu()

        choice = ui.getIntInput("Enter your choice: ")
        if choice == 1:
            ui.clearTerminal()
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
                data.createCsvFile()
                ui.addNutritionFailed(e)

        elif choice == 2:
            ui.clearTerminal()
            recipe = ui.getStringInput("Enter the name of the recipe to use from the Nutrition Entry List: ")
            entry = []
            try:
                entry = data.getEntryByName(recipe)

            except FileNotFoundError as e:
                data.createCsvFile()
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
                    data.createCsvFile()
                    ui.addNutritionFailed(e)
            else:
                ui.addNutritionFailed("Recipe not found in the nutrition entry list.")

        elif choice == 3:
            ui.clearTerminal()
            try:
                entries = data.getAllEntries()
                ui.showEntries(entries, "Nutrition Entries:")
            except FileNotFoundError as e:
                data.createCsvFile()
                ui.showEntriesFailed(e)
            except IndexError as e:
                ui.showEntriesFailed(e)

        elif choice == 4:
            ui.clearTerminal()
            stats_running = True
            while stats_running:
                ui.showStatisticsMenu()
                stats_choice = ui.getIntInput("Select statistics type: ")

                try:
                    if stats_choice == 1:
                        totals = data.getDailyTotals()
                        if totals:
                            ui.showEntries(totals, "Daily Total Intake")
                        else:
                            ui.showEntriesFailed("No entries found for today")
                        stats_running = False  # Exit stats menu after showing result
                    elif stats_choice == 2:
                        averages = data.getWeeklyAverages()
                        if averages:
                            ui.showEntries(averages, "Weekly Average Intake")
                        else:
                            ui.showEntriesFailed("No entries found for this week")
                        stats_running = False  # Exit stats menu after showing result
                    elif stats_choice == 3:
                        ui.clearTerminal()
                        stats_running = False  # Back to main menu
                    else:
                        ui.invalidChoice()
                        # Loop continues, will show menu again

                except FileNotFoundError as e:
                    data.createCsvFile()
                    ui.addNutritionFailed(e)
                    stats_running = False

        elif choice == 5:
            is_running = False
            ui.exitMessage()
            break

        else:
            ui.invalidChoice()

if __name__ == "__main__":
    main()
