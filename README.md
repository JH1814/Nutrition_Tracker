# 🍎 Nutrition Tracker

## About This Project
This project is intended to:
- Practice the complete process from problem analysis to implementation
- Apply basic Python programming concepts (console I/O, control flow, functions, modules)
- Demonstrate console interaction, data validation, and file processing
- Produce clean, well-structured, and documented code suitable for future teamwork
- Encourage frequent, incremental commits to track progress

## 📝 Analysis

### Problem
Many people track their daily nutrition manually using notes or spreadsheets, which often leads to **input errors, missing data**, and **no automatic** daily summaries.
A console-based tracker can simplify this process by storing entries in a structured format and generating quick overviews.

### Scenario 🧭
A user opens the program daily to record food items they’ve eaten — including date, category (e.g., protein, fat, carbs, sugar), and amount.
The program validates the inputs, saves them into a file, and allows users to view summaries like total calories or nutrients per day or week.

### User Stories 📘
1.	As a user, I want to **add food entries** with date, category, and quantity so I can track my nutrition.

2.	As a user, I want to **get a list of all entries** to have a full overview about what I ate.

3.	As a user, I want to **view my daily and weekly totals** to understand my intake.

4.	As a user, I want my data to be **saved and loaded automatically**, so I don’t lose progress.

5.	As a user, I want to be notified when I enter **invalid data** (e.g., wrong date or negative amount).

### Use Cases 🔧
* **Add Entry:** User inputs a new nutrition record.
* **List Entries:** Display all or filtered records.
* **Show Statistics:** Calculate and display daily or weekly totals.
* **Save / Load Entries:** Store and retrieve entries from a file (.json or .csv).
* **Exit:** Safely quit the program.

## Project Requirements ✅
### Each project must fulfill these three conditions:
1.	**Interactive App (console input)**
2.	**Data validation (input checking)**
3.	**File processing (read/write)**

### 1. Interactive App (Console Input)
The application interacts with the user via the console. Users can:
- Navigate a main menu and a statistics submenu
- Add nutrition entries (name, protein, fat, carbs, calories)
- Reuse an existing entry by name
- View all entries and see daily totals or weekly averages

Key UI functions in `src/ui.py`:
- `show_main_menu()`, `show_statistics_menu()` for navigation
- `get_string_input()`, `get_float_input()`, `get_int_input()` for validated input

### 2. Data Validation
All user input is validated to ensure data integrity and a smooth experience. Examples from `src/ui.py`:

```python
def get_string_input(message: str) -> str:
    is_valid = False
    while not is_valid:
        try:
            string = input(message)
            if not string or string.isdigit() or len(string) > 30:
                raise ValueError("Input Cannot be Empty, a Number, or Longer than 30 Characters.")
            is_valid = True
        except ValueError as e:
            print(f"Invalid Input. Please Enter a Valid String. {e}")
    return string
```

```python
def get_float_input(message: str) -> float:
    is_valid = False
    while not is_valid:
        try:
            number = float(input(message))
            is_valid = True
        except ValueError as e:
            print(f"Invalid Input. Please Enter a Valid Number. {e}")
    return number
```

```python
def get_int_input(message: str) -> int:
    is_valid = False
    while not is_valid:
        try:
            integer = int(input(message))
            is_valid = True
        except ValueError as e:
            print(f"Invalid Input. Please Enter a Valid Integer. {e}")
    return integer
```

Additional safeguards:
- **Name field length:** Limited to 30 characters (documented and enforced in `getStringInput`)
- **CSV data integrity:** All data retrieval functions skip rows with empty/missing `Name` fields using:
	```python
	if not row.get('Name', '').strip():
	    continue  # Skip corrupted row
	```
- **DateTime validation:** Entry timestamps are validated during reads; malformed dates are silently skipped:
	```python
	try:
	    entry_date = datetime.datetime.fromisoformat(row['DateTime'])
	except (ValueError, KeyError):
	    continue  # Skip invalid/missing datetime
	```
- **Numeric field validation:** Statistics calculations gracefully handle non-numeric values:
	```python
	try:
	    total_protein += float(entry.get('Protein', 0))
	except ValueError:
	    pass  # Skip malformed entries
	```
- **File system resilience:** Missing CSV files are automatically recreated with proper headers via `create_csv_file()`
- **Corruption detection:** `data.scan_csv_for_corruption()` scans the entire file and reports the count of invalid rows without blocking operations
- **Robust statistics display:** `ui.show_stats_result(...)` centralizes display and performs a single corruption scan with consistent messaging


### 3. File Processing
The application persists data in a CSV file (`src/data/data.csv`). The `src/data.py` module handles:
- File existence checks and automatic creation on demand
- Appending new entries with timestamps
- Reading entries safely, skipping corrupted rows
- Scanning the CSV for corruption and reporting counts

Illustrative patterns:
```python
# Append a row to CSV
with open(csv_file_path, 'a', newline='') as f:
    writer = csv.writer(f)
    writer.writerow([name, protein, fat, carbs, calories, datetime.datetime.now()])
```

```python
# Read all valid entries
with open(csv_file_path, 'r', newline='') as f:
    reader = csv.DictReader(f)
    for row in reader:
        if not row.get('Name', '').strip():
            continue  # skip corrupted
        entries.append(row)
```

## Filestructure 📂

Project layout (excluding the `testing` folder):

```
Nutrition_Tracker/
├── README.md                       # Project overview & user guide
├── PROGRAM_OVERVIEW.md             # Detailed architecture & feature docs
├── VALIDATION_DOCUMENTATION.md     # Validation logic explanations
├── FILE_PROCESSING_DOCUMENTATION.md# File I/O process details
├── USER_MANUAL.md                  # End-user manual
├── src/                            # Source code
│   ├── main.py                     # Entry point & main loop routing
│   ├── ui.py                       # Terminal UI & input validation
│   ├── data.py                     # Persistence + lookups + analytics
│   └── data/                       # Data storage directory
│       └── data.csv                # Persistent nutrition entries (CSV)
└── .git/                           # Git metadata
```

### Architecture Overview 🧱
- `main.py` (Flow Coordinator): Runs the loop, interprets user choices, dispatches operations.
- `ui.py` (Presentation / Interaction): Renders menus & tables, performs input validation loops.
- `data.py` (Data & Analytics): Handles file existence, CSV read/write, entry queries, daily/weekly computations, corruption scanning.
- `src/data/data.csv` (Storage): Flat append-only store of nutrition records.


Recent refactor highlights:
- Centralized statistics display and corruption warnings via `ui.showStatsResult(...)` to avoid duplicated logic.
- Simplified write path by removing redundant `data.checkCsvFileExists()` calls before writes; existence is handled once and on-demand on errors.
Potential evolution (future, not implemented yet) could split `data.py` into distinct service and repository modules and introduce a domain data class for structured entries.
### Visualization
### File / Module Roles 🗂️

Stats display helper:
- Call `ui.showStatsResult(data.getDailyTotals(), "Daily Total Intake", "No Entries Found for Today")` or with weekly averages to ensure consistent output and a single corruption scan.
- `main.py`: Application flow & routing.
- `ui.py`: Terminal interaction & validation.
- `data.py`: Persistence + queries + analytics.
- `data.csv`: Flat storage (append-only rows).

This layout minimizes indirection while keeping responsibilities clear for a small codebase.


### Flow (ASCII) 🔀
```
┌────────────────────────────┐
│ if __name__ == "__main__"  │
│        main()              │
└────────────┬───────────────┘
                         │
                         ▼
┌────────────────────────────┐
│ is_running = True          │
└────────────┬───────────────┘
                         │
                         ▼
┌──────────────────────────────────────────────────────────┐
│ MAIN LOOP (while is_running)                             │
│  1. data.checkCsvFileExists()                            │
│  2. ui.showMainMenu()                                    │
│  3. choice = ui.getIntInput("Enter your Choice:")        │
│  4. Route by choice                                      │
└────────────┬─────────────────────────────────────────────┘
                         │
     ┌─────────┼───────────────────────────────────────────────────────────────────────────────┐
     │         │                                                                                 │
     │         │ Choice == 1 (Add Entry)                                                         │
     │         │   ┌──────────────────────────────────────────────────────────────────────────┐  │
     │         │   │ ui.clearTerminal()                                                        │  │
     │         │   │ name = ui.getStringInput() (≤30 chars)                                    │  │
     │         │   │ protein = ui.getFloatInput()                                             │  │
     │         │   │ fat = ui.getFloatInput()                                                 │  │
     │         │   │ carbs = ui.getFloatInput()                                               │  │
     │         │   │ calories = ui.getFloatInput()                                            │  │
     │         │   │ data.checkCsvFileExists()                                                │  │
     │         │   │ data.writeNutritionData([... dt.now()])                                   │  │
     │         │   │ ui.addNutritionSuccessfull() | ui.addNutritionFailed(e)                   │  │
     │         │   └──────────────────────────────────────────────────────────────────────────┘  │
     │         │                                                                                 │
     │         │ Choice == 2 (Reuse Existing Entry)                                              │
     │         │   ┌──────────────────────────────────────────────────────────────────────────┐  │
     │         │   │ ui.clearTerminal()                                                        │  │
     │         │   │ recipe = ui.getStringInput()                                              │  │
     │         │   │ entry = data.getEntryByName(recipe)                                      │  │
     │         │   │ IF entry found:                                                          │  │
     │         │   │   data.checkCsvFileExists()                                              │  │
     │         │   │   data.writeNutritionData(copy + new timestamp)                          │  │
     │         │   │   ui.addNutritionSuccessfull()                                           │  │
     │         │   │ ELSE: ui.addNutritionFailed("Recipe Not Found")                         │  │
     │         │   └──────────────────────────────────────────────────────────────────────────┘  │
     │         │                                                                                 │
     │         │ Choice == 3 (View Entries)                                                      │
     │         │   ┌──────────────────────────────────────────────────────────────────────────┐  │
     │         │   │ ui.clearTerminal()                                                        │  │
     │         │   │ entries = data.getAllEntries()                                            │  │
     │         │   │ ui.showEntries(entries, "Nutrition Entries:")                           │  │
     │         │   │ corrupt = data.scanCsvForCorruption() → if >0 ui.showEntriesFailed(warn)  │  │
     │         │   └──────────────────────────────────────────────────────────────────────────┘  │
     │         │                                                                                 │
     │         │ Choice == 4 (Statistics Submenu)                                                │
     │         │   ┌──────────────────────────────────────────────────────────────────────────┐  │
     │         │   │ stats_running = True                                                      │  │
     │         │   │ WHILE stats_running:                                                      │  │
     │         │   │   ui.showStatisticsMenu()                                                 │  │
     │         │   │   stats_choice = ui.getIntInput()                                         │  │
     │         │   │   IF 1 (Daily Totals):                                                    │  │
     │         │   │     totals = data.getDailyTotals()                                        │  │
     │         │   │     IF totals: ui.showEntries(totals) ELSE ui.showEntriesFailed("None")  │  │
     │         │   │     data.scanCsvForCorruption() warning if needed                        │  │
     │         │   │     stats_running = False                                                 │  │
     │         │   │   IF 2 (Weekly Averages):                                                 │  │
     │         │   │     averages = data.getWeeklyAverages()                                   │  │
     │         │   │     IF averages: ui.showEntries(averages) ELSE ui.showEntriesFailed("None")│ │
     │         │   │     data.scanCsvForCorruption() warning if needed                        │  │
     │         │   │     stats_running = False                                                 │  │
     │         │   │   IF 3 (Back): stats_running = False                                      │  │
     │         │   └──────────────────────────────────────────────────────────────────────────┘  │
     │         │                                                                                 │
     │         │ Choice == 5 (Exit)                                                              │
     │         │   ┌──────────────────────────────────────────────────────────────────────────┐  │
     │         │   │ ui.exitMessage()                                                          │  │
     │         │   │ is_running = False                                                        │  │
     │         │   └──────────────────────────────────────────────────────────────────────────┘  │
     │         │                                                                                 │
     │         │ ELSE (Invalid Choice) → ui.invalidChoice()                                      │
     └─────────┘                                                                                 │
                         │                                                                                 │
                         ▼                                                                                 │
┌────────────────────────────┐                                                                 │
│ is_running == False ?      │◀────────────────────────────────────────────────────────────────┘
└────────────┬───────────────┘
                         │YES
                         ▼
┌────────────────────────────┐
│          EXIT               │
└────────────────────────────┘
                         │NO (loop) re-enters main while
                         └──▶ CONTINUE LOOP
```

### Flowchart 🗺️






<img width="1597" height="2262" alt="Readme_Flowchart_Programming drawio (4)" src="https://github.com/user-attachments/assets/455ef8fd-7ca1-41c0-8ee9-8e495540cad1" />













## 🧩 User Manual

The following section explains step-by-step how to use the **Nutrition Tracker** application.

---

### 1️. Start the Program 🚀

When you start the program, the **main menu** will appear in your terminal.

Example:
```
Welcome to Nutrition Tracker!

1. Add a new food entry
2. View all entries
3. View entries of the current week
4. Show statistics
5. Exit program
```

➡️ Choose an option by typing the number (1–5) and pressing **Enter**.

---

### 2️. Add a New Food Entry ➕

Select option **1** from the main menu.  
The program will ask you to enter information about your meal.

Example prompt:
```
Food name:
Protein (g):
Fat (g):
Carbs (g):
Calories (kcal):
```

Note: The app automatically records the current timestamp; no date entry is required.

✅ If all inputs are valid, your entry will be saved successfully.  
❌ If you enter invalid data (like empty text or wrong number format), the program will show an error message and ask again.

---

### 3️. View All Entries 📋

Select option **2** from the main menu.  
This will display all entries currently saved in the system.

Example output:
```
Chicken – 180 kcal
Rice – 200 kcal
Protein Shake – 250 kcal
```

➡️ Use this option to quickly see what you have eaten and how many calories you recorded.

---

### 4️. View Entries from the Current Week 🗓️

Select option **3** from the main menu.  
This will show all entries recorded **within the last 7 days** and also calculate the **total calories of the week**.

Example output:
```
Entries from this week:
- Pizza (850 kcal)
- Salad (300 kcal)
- Pasta (700 kcal)
Total calories this week: 1850 kcal
```

➡️ Use this to check your weekly calorie balance and track your eating habits.

---

### 5️. Show Statistics 📊

Select option **4** from the main menu.  
The program will display simple statistics based on your stored data.

Example output:
```
--- Weekly Statistics ---
Average calories/day: 925 kcal
Highest entry: Pizza (850 kcal)
Lowest entry: Salad (300 kcal)
```

➡️ This helps you analyze your nutrition over time.

---

### 6️. Exit the Program 🚪

Select option **5** to close the program.  
All your data will be saved automatically before the application exits.

Example:
```
Exiting program...
Goodbye!
```

➡️ Always use this option to ensure your data is stored correctly before closing the program.

---

### Summary of Menu Options

| Option | Description |
|:--:|:--|
| 1 | Add a new food entry |
| 2 | View all entries |
| 3 | View entries of the current week |
| 4 | Show weekly statistics |
| 5 | Exit the program |

---

### Tips 💡

- Always enter numbers (calories) without extra spaces or letters.  
- Timestamps are recorded automatically; you do not enter dates manually.  
- If the program displays an error, just follow the message and re-enter the correct value.  
- Use lowercase “yes” / “no” when the program asks for a confirmation (if implemented).  
- Names are limited to 30 characters; use concise, descriptive titles.  

---

Enjoy tracking your meals and managing your daily calories with the **Nutrition Tracker**! 🍎

## ⚙️ Implementation

### Technology
- Python 3.x
- No external libraries; uses Python standard library only

### How to Run
From the project root:

```bash
python3 src/main.py
```

### Libraries Used
- `os`, `time` (UI/terminal control and pauses)
- `csv`, `datetime` (file I/O and timestamps in data layer)

## 👥 Team & Contributions

| Name        | Contribution                                    |
|-------------|-------------------------------------------------|
| Raji        | Feature X / Y, documentation Z                  |
| Paulo       | Data functions, testing, refactor               |
| Jonas       | Data functions, testing, refactor               |

## 📝 License
This project is a graded group work for the programming foundation module.
