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
    pass

def getEntryByDate(date):

    pass

def getEntryByName(name):
    pass

def getEntriesWithinWeek(): #get the entries within last 7 days
    entries = []
    one_week_ago = datetime.datetime.now() - datetime.timedelta(days=7)

    with open("./data/data.csv",'r') as file:
        # Use DictReader to treat each row as a dictionary with column headers as keys
        reader = csv.DictReader(file)
        for row in reader:
            # Check if the entry is within the last 7 days
            entry_date = datetime.strptime(row['DateTime'], '%Y-%m-%d')
            if entry_date >= one_week_ago:
                entries.append(row)

    return entries


#statistics functions
def createStatistics():
    pass

#validation functions
def validateFloat(input):
    pass

def validateStr(input): #Not empty
    pass

def validateInt(input): #return int(input) or raise error
    pass