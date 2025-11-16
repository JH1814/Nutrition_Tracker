import csv
import datetime

def writeNutritionData(data):
    with open("./data/data.csv", "a") as file:
        writer = csv.writer(file)
        writer.writerow(data)

#request data functions
def getAllEntries():
    entries = []
    with open("./data/data.csv",'r') as file:
        # Use DictReader to treat each row as a dictionary with column headers as keys
        reader = csv.DictReader(file)
        for row in reader:
            entries.append(row)
        
    return entries

def getEntriesByDate(date = datetime.datetime.now().date()): #get the entries of today
    entries = []

    with open("./data/data.csv",'r') as file:
        # Use DictReader to treat each row as a dictionary with column headers as keys
        reader = csv.DictReader(file)
        for row in reader:
            # Check if the entry is within the last 7 days
            entry_date = datetime.datetime.fromisoformat(row['DateTime']).date()
            if entry_date == date:
                entries.append(row)

    return entries

def getEntriesWithinWeek(): #get the entries within last 7 days
    entries = []
    one_week_ago = datetime.datetime.now() - datetime.timedelta(days=7)

    with open("./data/data.csv",'r') as file:
        # Use DictReader to treat each row as a dictionary with column headers as keys
        reader = csv.DictReader(file)
        for row in reader:
            # Check if the entry is within the last 7 days
            entry_date = datetime.datetime.fromisoformat(row['DateTime'])
            if entry_date >= one_week_ago:
                entries.append(row)

    return entries

def getEntryByName(name):
    entry = []
    with open("./data/data.csv",'r') as file:
        # Use DictReader to treat each row as a dictionary with column headers as keys
        reader = csv.DictReader(file)
        for row in reader:
            if row['Name'] == name:
                entry.append(row)
                break

    return entry

def createCsvFile():
    with open("./data/data.csv", "w") as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Protein", "Fat", "Carbs", "Calories", "DateTime"])

def checkCsvFileExists():
    exists = False
    while not exists:
        try:
            with open("./data/data.csv", "r") as file:
                exists = True
        except FileNotFoundError:
            createCsvFile()

#statistics functions
def getDailyTotals():
    """Calculate daily totals for Protein, Fat, Carbs, Calories for a specific date."""
    
    entries = getEntriesByDate()

    if not entries:
        return None
    
    # Initialize totals
    total_protein = 0.0
    total_fat = 0.0
    total_carbs = 0.0
    total_calories = 0.0

    # Sum all values
    for entry in entries:
        try:
            total_protein += float(entry.get('Protein', 0))
            total_fat += float(entry.get('Fat', 0))
            total_carbs += float(entry.get('Carbs', 0))
            total_calories += float(entry.get('Calories', 0))
        except ValueError:
            pass  # Skip malformed entries
    
    return [{
        'Protein': round(total_protein, 2), 
        'Fat': round(total_fat, 2), 
        'Carbs': round(total_carbs, 2), 
        'Calories': round(total_calories, 2)
        }]
    

def getWeeklyAverages():
    """Calculate weekly averages for Protein, Fat, Carbs, Calories."""
    entries = getEntriesWithinWeek()
    
    if not entries:
        return None
    
    # Initialize totals
    total_protein = 0.0
    total_fat = 0.0
    total_carbs = 0.0
    total_calories = 0.0
    
    # Sum all values
    for entry in entries:
        try:
            total_protein += float(entry.get('Protein', 0))
            total_fat += float(entry.get('Fat', 0))
            total_carbs += float(entry.get('Carbs', 0))
            total_calories += float(entry.get('Calories', 0))
        except ValueError:
            pass  # Skip malformed entries
    
    # Calculate averages
    count = len(entries)
    return [{
        'Protein': round(total_protein / count, 2),
        'Fat': round(total_fat / count, 2),
        'Carbs': round(total_carbs / count, 2),
        'Calories': round(total_calories / count, 2)
    }]