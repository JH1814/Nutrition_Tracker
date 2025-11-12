# Nutrition Tracker
## Problem
Many people track their daily nutrition manually using notes or spreadsheets, which often leads to **input errors, missing data**, and **no automatic** daily summaries.
A console-based tracker can simplify this process by storing entries in a structured format and generating quick overviews.

## Scenario
A user opens the program daily to record food items they’ve eaten — including date, category (e.g., protein, fat, carbs, sugar), and amount.
The program validates the inputs, saves them into a file, and allows users to view summaries like total calories or nutrients per day or week.

## User Stories
1.	As a user, I want to **add food entries** with date, category, and quantity so I can track my nutrition.

2.	As a user, I want to **get a list of all entries** to have a full overview about what I ate.

3.	As a user, I want to **view my daily and weekly totals** to understand my intake.

4.	As a user, I want my data to be **saved and loaded automatically**, so I don’t lose progress.

5.	As a user, I want to be notified when I enter **invalid data** (e.g., wrong date or negative amount).

## Use Cases
* **Add Entry:** User inputs a new nutrition record.
* **List Entries:** Display all or filtered records.
* **Show Statistics:** Calculate and display daily or weekly totals.
* **Save / Load Entries:** Store and retrieve entries from a file (.json or .csv).
* **Exit:** Safely quit the program.

## Project Requirements
### Each project must fulfill these three conditions:
1.	**Interactive App (console input)**
2.	**Data validation (input checking)**
3.	**File processing (read/write)**






## Filestructure  

Our project uses the **MVC structure (Model - View - Controller)**.  
This structure helps to keep the code clean, organized, and easy to maintain.

### Model
The Model handles all data operations.  
It reads and writes data from the `data.csv` file and contains the main program logic such as calculations and data validation.

### View
The View is responsible for displaying information to the user.  
It shows menus, messages, and outputs in the console.

### Controller
The Controller manages the connection between the Model and the View.  
It receives user input, decides what to do, and coordinates actions between data and output.

### main.py
The `main.py` file is the entry point of the program.  
It starts the Controller and connects all parts of the application.

### data.csv
The `data.csv` file stores all saved user data.  
It is used by the Model for loading and saving information.