import csv


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
    pass

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