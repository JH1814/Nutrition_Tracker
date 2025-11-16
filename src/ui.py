# includes functions to display menus
# includes functions to show nutrition entries
import os
import time

def showMainMenu():
    clearTerminal()
    print("Welcome to the Nutrition Tracker!")
    print("1. Add Nutrition Entry")
    print("2. Use Recipe from the Nutrition Entry List")
    print("3. View Nutrition Entries")
    print("4. View Statistics")
    print("5. Exit")

def showStatisticsMenu():
    clearTerminal()
    print("Statistics Menu:")
    print("1. Daily Statistics")
    print("2. Weekly Statistics")
    print("3. Back to Main Menu")

def showEntries(entries, message):
    clearTerminal()
    if not entries:
        showEntriesFailed("No entries found.")
        return

    print(message)
    # create header
    headers = ["Name", "Protein ", "Fat", "Carbs", "Calories"]
    print(f"{headers[0]:<30} {headers[1]:<10} {headers[2]:<10} {headers[3]:<10} {headers[4]:<10}")
    print("-" * 80)

    for entry in entries:
        name = entry.get('Name', '')
        protein = f"{entry.get('Protein', '')}g"
        fat = f"{entry.get('Fat', '')}g"
        carbs = f"{entry.get('Carbs', '')}g"
        calories = f"{entry.get('Calories', '')} kcal"
        print(f"{name:<30} {protein:<10} {fat:<10} {carbs:<10} {calories:<10}")
    
    input("\nPress Enter to continue...")
    clearTerminal()

def showEntriesFailed(error):
    clearTerminal()
    print(f"No entries found: {error}")
    time.sleep(1)

def addNutritionSuccessfull():
    clearTerminal()
    print("Nutrition data added successfully!")
    time.sleep(1)

def addNutritionFailed(error):
    clearTerminal()
    print(f"Failed to add nutrition data: {error}")
    time.sleep(1)
    clearTerminal()

def invalidChoice():
    clearTerminal()
    print("Invalid choice. Please try again.")
    time.sleep(1)
    clearTerminal()

def getStringInput(message):  
    is_valid = False
    while not is_valid:
        try: 
            string = input(message)
            if not string:
                raise ValueError("Input cannot be empty.")
            is_valid = True
        except ValueError as e:
            print(f"Invalid input. Please enter a valid string. {e}")
    return string

def getFloatInput(message):
    is_valid = False
    while not is_valid:
        try: 
            number = float(input(message))
            is_valid = True
        except ValueError as e:
            print(f"Invalid input. Please enter a valid number. {e}")
    return number

def getIntInput(message):
    is_valid = False
    while not is_valid:
        try: 
            integer = int(input(message))
            is_valid = True
        except ValueError as e:
            print(f"Invalid input. Please enter a valid integer. {e}")
    return integer

def clearTerminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def exitMessage():
    clearTerminal()
    print("Exiting the Nutrition Tracker. Goodbye!")
    time.sleep(1)
    clearTerminal()

