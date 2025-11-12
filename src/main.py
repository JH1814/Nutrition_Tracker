import data
import ui
import datetime

running = True

def main():
 while running:
    ui.showMainMenu()
    choice = input("Enter your choice: ")
    if choice == "1":
        name = print("Add Name of Nutrition Entry")
        carbs = print("Add Carbs in grams")
        protein = print("Add Protein in grams")
        fats = print("Add Fats in grams")
        date = datetime.datetime.now()

        try :
            data.writeNutritionData({"Name": name, "Carbs": carbs, "Protein": protein, "Fats": fats, "Date": date})
            ui.addNutritionSuccessfull()
        except FileNotFoundError as e:
            ui.addNutritionFailed(e)

    if choice == "2":
        recipie = input("Enter the name of the recipe to use from the Nutrition Entry List: ")
        entries = data.getEntryByName(recipie)
       
        try :
            data.writeNutritionData({"Name": entries.name, "Carbs": entries.carbs, "Protein": entries.protein, "Fats": fats, "Date": entries.date})
            ui.addNutritionSuccessfull()
        except FileNotFoundError as e:
            ui.addNutritionFailed(e)

# if choice =="5":
    #running = False
    #exit()





if __name__ == "__main__":
    main()
