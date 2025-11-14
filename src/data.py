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


def getEntryByDate(date = datetime.datetime.now().date()): #get the entries of today
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

def createHeader():
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
            createHeader()

#statistics functions
def createStatistics():
    pass