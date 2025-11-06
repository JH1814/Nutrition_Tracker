import data
import ui

running = True

def main():
 while running:
    ui.showMainMenu()
    choice = input("Enter your choice: ")
    if choice == "1":

        # ui.getNutritionInput()  # This function would get user input for nutrition data

# if choice =="5":
    #running = False
    #exit()

        try :
            data.writeNutritionData({date: "2024-06-01", protein: 50, carbs: 200, fats: 70})
            ui.addNutritionSuccessfull()
        except FileNotFoundError as e:
            ui.addNutritionFailed(e)





if __name__ == "__main__":
    main()
