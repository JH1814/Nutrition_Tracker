# includes functions to display menus
# includes functions to show nutrition entries
# 

def showMainMenu():
    print("Welcome to the Nutrition Tracker!")
    print("1. Add Nutrition Entry")
    print("2. Use Recipe from the Nutrition Entry List")
    print("3. View Nutrition Entries")
    print("4. View Statistics")
    print("5. Exit")

def addNutritionSuccessfull():
    print("Nutrition data added successfully!")

def addNutritionFailed(error):
    print(f"Failed to add nutrition data: {error}")

def getNutritionInput(): 
    pass

def showStatistics():
    pass

def showEntries(entries):
    pass