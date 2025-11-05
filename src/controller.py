# get called by main.py to handle user input and interact with the model and view
# gets menu from view and presents it to the user
# gets user input from view and processes it
# calls model functions to update or retrieve data
# calls view functions to display data to the user

import model
import view

running = True

def startApp():
 while running:
    view.showMainMenu()
    choice = input("Enter your choice: ")
    if choice == "1":

        # view.getNutritionInput()  # This function would get user input for nutrition data

# if choice =="5":
    #running = False
    #exit()

        try :
            model.writeNutritionData({date: "2024-06-01", protein: 50, carbs: 200, fats: 70})
            view.addNutritionSuccessfull()
        except FileNotFoundError as e:
            view.addNutritionFailed(e)

            

