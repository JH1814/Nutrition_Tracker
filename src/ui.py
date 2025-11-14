# includes functions to display menus
# includes functions to show nutrition entries


def showMainMenu():
    print("Welcome to the Nutrition Tracker!")
    print("1. Add Nutrition Entry")
    print("2. Use Recipe from the Nutrition Entry List")
    print("3. View Nutrition Entries")
    print("4. View Statistics")
    print("5. Exit")

def showStatisticsMenu():
    print("Statistics Menu:")
    print("1. Daily Statistics")
    print("2. Weekly Statistics")
    print("3. Back to Main Menu")

def showDailyAverages(averages):
    """Display daily average nutrition statistics."""
    if not averages:
        print("No entries found for this day.")
        return
    
    print("\n" + "="*60)
    print(f"DAILY AVERAGE NUTRITION STATISTICS - {averages['Date']}")
    print("="*60)
    print(f"Total entries today: {averages['Count']}")
    print("-"*60)
    print(f"Average Protein:  {averages['Protein']:.2f} g")
    print(f"Average Fat:      {averages['Fat']:.2f} g")
    print(f"Average Carbs:    {averages['Carbs']:.2f} g")
    print(f"Average Calories: {averages['Calories']:.2f} kcal")
    print("="*60 + "\n")

def showWeeklyAverages(averages):
    """Display weekly average nutrition statistics."""
    if not averages:
        print("No entries found for this week.")
        return
    
    print("\n" + "="*60)
    print("WEEKLY AVERAGE NUTRITION STATISTICS")
    print("="*60)
    print(f"Total entries this week: {averages['Count']}")
    print("-"*60)
    print(f"Average Protein:  {averages['Protein']:.2f} g/day")
    print(f"Average Fat:      {averages['Fat']:.2f} g/day")
    print(f"Average Carbs:    {averages['Carbs']:.2f} g/day")
    print(f"Average Calories: {averages['Calories']:.2f} kcal/day")
    print("="*60 + "\n")

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

