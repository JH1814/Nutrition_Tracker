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
All user input is validated to ensure data integrity and a smooth experience. The project includes comprehensive validation with upper bounds and type checking.

**Enhanced Validation Constants** (in `src/ui.py`):
```python
MAX_NAME_LENGTH: int = 30
MAX_NUMERIC_VALUE: float = 10000.0  # Reasonable upper limit for nutrition values
```

**Input Validation Functions with Full Type Hints**:

```python
def get_string_input(message: str) -> str:
    """Get validated string input from user.
    
    Args:
        message: Prompt message to display
        
    Returns:
        Valid non-empty string (≤30 chars, not a number)
        
    Note:
        Loops until valid input is provided
    """
    is_valid = False
    while not is_valid:
        try:
            string = input(message)
            if not string or string.isdigit() or len(string) > MAX_NAME_LENGTH:
                raise ValueError(f"Input Cannot be Empty, a Number, or Longer than {MAX_NAME_LENGTH} Characters.")
            is_valid = True
        except ValueError as e:
            print(f"Invalid Input. Please Enter a Valid String. {e}")
    return string
```

```python
def get_float_input(message: str) -> float:
    """Get validated float input from user.
    
    Args:
        message: Prompt message to display
        
    Returns:
        Valid non-negative float value (0 to 10000)
        
    Note:
        Loops until valid input is provided
    """
    is_valid = False
    while not is_valid:
        try:
            number = float(input(message))
            if number < 0:
                raise ValueError("Input Cannot be Negative.")
            if number > MAX_NUMERIC_VALUE:
                raise ValueError(f"Input Cannot Exceed {MAX_NUMERIC_VALUE}.")
            is_valid = True
        except ValueError as e:
            print(f"Invalid Input. Please Enter a Valid Number. {e}")
    return number
```

```python
def get_int_input(message: str) -> int:
    """Get validated integer input from user.
    
    Args:
        message: Prompt message to display
        
    Returns:
        Valid non-negative integer value (0 to 10000)
        
    Note:
        Loops until valid input is provided
    """
    is_valid = False
    while not is_valid:
        try:
            integer = int(input(message))
            if integer < 0:
                raise ValueError("Input Cannot be Negative.")
            if integer > MAX_NUMERIC_VALUE:
                raise ValueError(f"Input Cannot Exceed {int(MAX_NUMERIC_VALUE)}.")
            is_valid = True
        except ValueError as e:
            print(f"Invalid Input. Please Enter a Valid Integer. {e}")
    return integer
```

**Additional Safeguards:**
- **Name field length:** Limited to 30 characters (enforced in `get_string_input`)
- **Upper bounds:** All numeric inputs validated to not exceed 10,000 (prevents unrealistic values)
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
- **Robust statistics display:** `ui.show_entries(...)` centralizes display and performs a single corruption scan with consistent messaging
- **Standardized error messages:** All error messages use consistent "Error:" prefix and remain visible for 2 seconds for better user experience


### 3. File Processing
The application persists data in a CSV file (`src/data/data.csv`). The `src/data.py` module handles all file operations with proper error handling and CSV best practices.

**Key Features:**
- **Module-relative path resolution:** CSV path automatically calculated relative to `data.py` location
- **Automatic file creation:** Missing CSV files recreated with proper headers via `create_csv_file()`
- **Proper CSV handling:** Uses `newline=''` parameter for correct cross-platform newline handling
- **Safe appending:** New entries written with timestamps without corrupting existing data
- **Resilient reading:** Safely reads entries, automatically skipping corrupted rows
- **Corruption detection:** `scan_csv_for_corruption()` reports count of invalid rows without blocking operations
- **Comprehensive type hints:** All functions fully typed with `list[dict[str, str]]`, etc.
- **Detailed docstrings:** Every function documented with Args, Returns, Raises, and Notes sections

**Illustrative patterns:**
```python
# Append a row to CSV with proper newline handling
with open(csv_file_path, 'a', newline='') as f:
    writer = csv.writer(f)
    writer.writerow([name, protein, fat, carbs, calories, datetime.datetime.now()])
```

```python
# Read all valid entries with DictReader for named access
with open(csv_file_path, 'r', newline='') as f:
    reader = csv.DictReader(f)
    for row in reader:
        if not row.get('Name', '').strip():
            continue  # skip corrupted rows
        entries.append(row)
```

**Data module structure:**
- File operations: `check_csv_file_exists()`, `create_csv_file()`, `write_nutrition_data()`
- Retrieval: `get_all_entries()`, `get_entries_by_date()`, `get_entries_within_week()`, `get_entry_by_name()`
- Quality: `scan_csv_for_corruption()`
- Analytics: `get_daily_totals()`, `get_weekly_averages()`

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
- **`main.py` (Flow Coordinator)**: Application entry point with module docstring. Runs the main loop, interprets user choices, dispatches operations to ui and data modules. Includes exception handling for each menu choice.
- **`ui.py` (Presentation / Interaction)**: Terminal interface with comprehensive type hints. Renders menus & tables, performs input validation with upper bounds (`MAX_NAME_LENGTH = 30`, `MAX_NUMERIC_VALUE = 10000.0`). All functions fully documented with Args/Returns/Note sections. Implements standardized error messages with "Error:" prefix and 2-second visibility.
- **`data.py` (Data & Analytics)**: Persistence layer with full type hints including `Optional` imports. Handles CSV operations with `newline=''` parameter, entry queries, daily/weekly analytics, and corruption scanning. All functions documented with comprehensive docstrings.
- **`src/data/data.csv` (Storage)**: Flat append-only store of nutrition records with columns: Name, Protein, Fat, Carbs, Calories, DateTime.

**Key improvements implemented:**
- Comprehensive type hints on all functions (e.g., `list[dict[str, str | float]]`)
- Module-level and function-level docstrings following Google/NumPy style
**Key improvements implemented:**
- Comprehensive type hints on all functions (e.g., `list[dict[str, str | float]]`)
- Module-level and function-level docstrings following Google/NumPy style
- Validation constants for consistent input bounds
- Enhanced error handling with standardized messaging
- CSV best practices with newline parameter for cross-platform compatibility
- PEP 8 compliant snake_case naming throughout

- **`main.py`**: Application entry point (now ~150 lines, was ~110 in main() alone). Clean handler functions: `handle_add_entry()`, `handle_reuse_entry()`, `handle_view_entries()`, `handle_statistics()`, `handle_exit()`. Main loop uses handler dictionary for elegant dispatch.
- **`ui.py`**: Terminal interface with 12+ typed functions. Input validation with constants (`MAX_NAME_LENGTH: int = 30`, `MAX_NUMERIC_VALUE: float = 10000.0`), display functions for menus/tables/stats, standardized error messages with "Error:" prefix and 2-second visibility.
- **`data.py`**: Data persistence and analytics with pure computation functions. **Pure functions** (no I/O): `compute_totals()`, `compute_averages()`. **I/O wrappers**: `get_all_entries()`, `get_entries_by_date()`, `get_daily_totals()`, `get_weekly_averages()`, `scan_csv_for_corruption()`.
- **`data.csv`**: Flat storage with append-only rows (Name, Protein, Fat, Carbs, Calories, DateTime).

**Pure function benefits:**
```python
# Pure computation - no I/O, easier to test
result = data.compute_totals(entries, 'Daily Total')

# I/O wrapper - clean separation of concerns
def get_daily_totals() -> list[dict] | None:
    entries = get_entries_by_date()  # I/O
    return compute_totals(entries, 'Daily Total')  # Pure computation
```

This layout minimizes indirection while keeping responsibilities clear. Type hints, docstrings, pure functions, and handler pattern ensure excellent maintainability.

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
│  1. data.check_csv_file_exists()                         │
│  2. ui.show_main_menu()                                  │
│  3. choice = ui.get_int_input("Enter your Choice:")      │
│  4. Route by choice                                      │
└────────────┬─────────────────────────────────────────────┘
                         │
     ┌─────────┼───────────────────────────────────────────────────────────────────────────────┐
     │         │                                                                                 │
     │         │ Choice == 1 (Add Entry)                                                         │
     │         │   ┌──────────────────────────────────────────────────────────────────────────┐  │
     │         │   │ ui.clear_terminal()                                                       │  │
     │         │   │ name = ui.get_string_input() (≤30 chars)                                  │  │
     │         │   │ protein = ui.get_float_input()                                            │  │
     │         │   │ fat = ui.get_float_input()                                                │  │
     │         │   │ carbs = ui.get_float_input()                                              │  │
     │         │   │ calories = ui.get_float_input()                                           │  │
     │         │   │ data.write_nutrition_data([... dt.now()])                                 │  │
     │         │   │ ui.add_nutrition_successful() | ui.add_nutrition_failed(e)                │  │
     │         │   └──────────────────────────────────────────────────────────────────────────┘  │
     │         │                                                                                 │
     │         │ Choice == 2 (Reuse Existing Entry)                                              │
     │         │   ┌──────────────────────────────────────────────────────────────────────────┐  │
     │         │   │ ui.clear_terminal()                                                       │  │
     │         │   │ recipe = ui.get_string_input()                                            │  │
     │         │   │ entry = data.get_entry_by_name(recipe)                                    │  │
     │         │   │ IF entry found:                                                           │  │
     │         │   │   data.write_nutrition_data(copy + new timestamp)                         │  │
     │         │   │   ui.add_nutrition_successful()                                           │  │
     │         │   │ ELSE: ui.add_nutrition_failed("Recipe Not Found")                         │  │
     │         │   └──────────────────────────────────────────────────────────────────────────┘  │
     │         │                                                                                 │
     │         │ Choice == 3 (View Entries)                                                      │
     │         │   ┌──────────────────────────────────────────────────────────────────────────┐  │
     │         │   │ ui.clear_terminal()                                                       │  │
     │         │   │ entries = data.get_all_entries()                                          │  │
     │         │   │ ui.show_entries(entries, "Nutrition Entries:", "No Entries Found.")  │  │
     │         │   └──────────────────────────────────────────────────────────────────────────┘  │
     │         │                                                                                 │
     │         │ Choice == 4 (Statistics Submenu)                                                │
     │         │   ┌──────────────────────────────────────────────────────────────────────────┐  │
     │         │   │ stats_running = True                                                      │  │
     │         │   │ WHILE stats_running:                                                      │  │
     │         │   │   ui.show_statistics_menu()                                               │  │
     │         │   │   stats_choice = ui.get_int_input()                                       │  │
     │         │   │   IF 1 (Daily Totals):                                                    │  │
     │         │   │     totals = data.get_daily_totals()                                      │  │
     │         │   │     ui.show_entries(totals, "Daily Total", "No Entries for Today")   │  │
     │         │   │     stats_running = False                                                 │  │
     │         │   │   IF 2 (Weekly Averages):                                                 │  │
     │         │   │     averages = data.get_weekly_averages()                                 │  │
     │         │   │     ui.show_entries(averages, "Weekly Avg", "No Entries this Week")  │  │
     │         │   │     stats_running = False                                                 │  │
     │         │   │   IF 3 (Back): stats_running = False                                      │  │
     │         │   └──────────────────────────────────────────────────────────────────────────┘  │
     │         │                                                                                 │
     │         │ Choice == 5 (Exit)                                                              │
     │         │   ┌──────────────────────────────────────────────────────────────────────────┐  │
     │         │   │ ui.exit_message()                                                         │  │
     │         │   │ is_running = False                                                        │  │
     │         │   └──────────────────────────────────────────────────────────────────────────┘  │
     │         │                                                                                 │
     │         │ ELSE (Invalid Choice) → ui.invalid_choice()                                     │
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

### Simple Flow Sketch ▶️
Start → show_main_menu() → get_int_input() →
• If 1: get_string_input()/get_float_input() → write_nutrition_data() → add_nutrition_successful()
• If 2: get_string_input() → get_entry_by_name() → write_nutrition_data() → add_nutrition_successful()
• If 3: get_all_entries() → show_entries()
• If 4: show_statistics_menu() → get_int_input() → get_daily_totals()/get_weekly_averages() → show_entries()
• If 5: exit_message() → End


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

- **Input validation**: All numeric inputs are validated for range (0 to 10,000) and type. Invalid inputs trigger error messages with 2-second visibility before retry.
- **Names limited to 30 characters**: Use concise, descriptive titles for food entries.
- **Type hints throughout**: All functions use Python type hints for better IDE support and code clarity.
- **Error messages**: Look for "Error:" prefix in all error messages. Terminal won't clear immediately after errors, giving you time to read them.
- **Timestamps automatic**: The app records current date/time automatically when you add entries.
- **Upper bounds protection**: System prevents unrealistic values (e.g., 50,000 calories) by capping inputs at 10,000.
- **CSV format**: Data stored with proper `newline=''` parameter for cross-platform compatibility.
- **Documentation**: All functions include comprehensive docstrings with Args/Returns/Note sections.

---

Enjoy tracking your meals and managing your daily calories with the **Nutrition Tracker**! 🍎

## ⚙️ Implementation

### Technology
- **Python 3.x**: Standard library only, no external dependencies
- **Type hints**: Comprehensive typing throughout with `Optional`, `list[dict[str, str | float]]`, etc.
- **Docstrings**: Module and function-level documentation following Google/NumPy style
- **PEP 8 compliance**: snake_case naming conventions throughout
- **Pure functions**: Computation separated from I/O for testability (`compute_totals`, `compute_averages`)
- **Handler pattern**: Menu dispatch via dictionary routing (src/main.py)

### How to Run
From the project root:

```bash
python3 src/main.py
```

### Libraries Used
- `os`, `time`: UI/terminal control and pauses
- `csv`, `datetime`: File I/O and timestamps in data layer

### Code Quality Features
- **Validation constants**: `MAX_NAME_LENGTH = 30`, `MAX_NUMERIC_VALUE = 10000.0`
- **Standardized error messages**: Consistent "Error:" prefix, 2-second visibility
- **CSV best practices**: Proper `newline=''` parameter on all file operations
- **Comprehensive type hints**: All function parameters and returns typed
- **Detailed docstrings**: Every function documented with purpose, arguments, returns, and notes
- **Handler pattern**: 6 focused functions replacing monolithic main() (110 → ~163 lines with improved readability)
- **Pure functions**: Separated computation from I/O (compute_totals, compute_averages) for 100% testability

## 👥 Team & Contributions

| Name        | Contribution                                    |
|-------------|-------------------------------------------------|
| Raji        | Documentation, Main flow                        |
| Paulo       | UI functions, Main flow                         |
| Jonas       | Data functions, Main flow                       |

## 📝 License
This project is a graded group work for the programming foundation module.
