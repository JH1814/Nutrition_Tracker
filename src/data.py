import csv
import datetime



def writeNutritionData(data):
    with open("./data/data.csv", "a") as file:
        writer = csv.writer(file)
        writer.writerow(data)

def addEntry(data):
    pass

#request data functions
def getAllEntries():
    entries = []
    with open("./data/data.csv",'r') as file:
        # Use DictReader to treat each row as a dictionary with column headers as keys
        reader = csv.DictReader(file)
        for i in range(10):
            row = next(reader)
            entries.append(row)
        
    return entries

def getEntryByDate(): #get the entries of today
    entries = []
    today = datetime.datetime.now().date()

    with open("./data/data.csv",'r') as file:
        # Use DictReader to treat each row as a dictionary with column headers as keys
        reader = csv.DictReader(file)
        for row in reader:
            # Check if the entry is within the last 7 days
            entry_date = datetime.datetime.fromisoformat(row['DateTime']).date()
            if entry_date == today:
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

#statistics functions
def createStatistics():
    pass