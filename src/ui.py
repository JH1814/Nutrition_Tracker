# includes functions to display menus
# includes functions to show nutrition entries
import os
import time

def showMainMenu() -> None:
    clearTerminal()
    print("Welcome to the Nutrition Tracker!")
    print("1. Add Nutrition Entry")
    print("2. Use Existing Nutrition Entry")
    print("3. View Nutrition Entries")
    print("4. View Statistics")
    print("5. Exit")

def showStatisticsMenu() -> None:
    clearTerminal()
    print("Statistics Menu:")
    print("1. Daily Totals")
    print("2. Weekly Averages")
    print("3. Back to Main Menu")

def showEntries(entries: list, message: str) -> None:
    clearTerminal()
    if not entries:
        showEntriesFailed("No Entries Found.")
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

def showEntriesFailed(error: str) -> None:
    clearTerminal()
    print(f"No Entries Found: {error}")
    time.sleep(1)

def addNutritionSuccessfull() -> None:
    clearTerminal()
    print("Nutrition Data Added Successfully!")
    time.sleep(1)

def addNutritionFailed(error: str) -> None:
    clearTerminal()
    print(f"Failed to Add Nutrition Data: {error}")
    time.sleep(1)
    clearTerminal()

def invalidChoice() -> None:
    clearTerminal()
    print("Invalid Choice. Please Try Again.")
    time.sleep(1)
    clearTerminal()

def getStringInput(message: str) -> str:  
    is_valid = False
    while not is_valid:
        try: 
            string = input(message)
            if not string or string.isdigit():
                raise ValueError("Input Cannot be Empty or a Number.")
            is_valid = True
        except ValueError as e:
            print(f"Invalid Input. Please Enter a Valid String. {e}")
    return string

def getFloatInput(message: str) -> float:
    is_valid = False
    while not is_valid:
        try: 
            number = float(input(message))
            is_valid = True
        except ValueError as e:
            print(f"Invalid Input. Please Enter a Valid Number. {e}")
    return number

def getIntInput(message: str) -> int:
    is_valid = False
    while not is_valid:
        try: 
            integer = int(input(message))
            is_valid = True
        except ValueError as e:
            print(f"Invalid Input. Please Enter a Valid Integer. {e}")
    return integer

def clearTerminal() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')

def exitMessage() -> None:
    clearTerminal()
    print("Exiting the Nutrition Tracker. Goodbye!")
    time.sleep(2)
    clearTerminal()

