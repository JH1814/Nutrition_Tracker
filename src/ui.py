# includes functions to display menus
# includes functions to show nutrition entries


def showMainMenu():
    print("Welcome to the Nutrition Tracker!")
    print("1. Add Nutrition Entry")
    print("2. Use Recipe from the Nutrition Entry List")
    print("3. View Nutrition Entries")
    print("4. View Statistics")
    print("5. Exit")

def showStatistics():
    pass

def showEntries(entries):

    if not entries:
        print("No entries found.")
        return

    # create header
    headers = ["Name", "Protein", "Fat", "Carbs", "Calories"]
    print(f"{headers[0]:<30} {headers[1]:<10} {headers[2]:<10} {headers[3]:<10} {headers[4]:<10}")
    print("-" * 80)

    for entry in entries:
        print(f"{entry.get('Name',''):<30} {entry.get('Protein',''):<10} {entry.get('Fat',''):<10} {entry.get('Carbs',''):<10} {entry.get('Calories',''):<10}")

def showEntriesFailed(error):
    print(f"No entries found: {error}")

def addNutritionSuccessfull():
    print("Nutrition data added successfully!")

def addNutritionFailed(error):
    print(f"Failed to add nutrition data: {error}")

def invalidChoice():
    print("Invalid choice. Please try again.")

def getStringInput(message):  #not null string
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

