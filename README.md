# 🍎 Nutrition Tracker

## 📝 Analysis

### Problem
Many people **track** their daily **nutrition** manually using notes or spreadsheets, which often leads to **input errors, missing data**, and **no automatic** daily summaries.
A console-based tracker can simplify this process by storing entries in a structured format and generating quick overviews.

### Scenario 🧭
A user opens the program daily to record food items they’ve eaten including date, category (e.g., protein, fat, carbs, sugar), and amount.
The program validates the inputs, saves them into a file, and allows users to view summaries like total calories or nutrients per day or week.

### User Stories 📘
1.	As a user, I want to **add food entries** with date, category, and quantity so I can track my nutrition.

2.	As a user, I want to **get a list of all entries** to have a full overview about what I ate.

3.	As a user, I want to **view my daily and weekly totals** to understand my intake.

4.	As a user, I want my data to be **stored permanently**, so I don’t lose progress.

5.	As a user, I want to **be notified** when I enter **invalid data** (e.g., wrong date or negative amount) so data is stored correctly.

### Use Cases 🔧
* **Add Entry:** User inputs a new nutrition record.
* **List Entries:** Display all or filtered records.
* **Show Statistics:** Calculate and display daily or weekly totals.
* **Save / Load Entries:** Store and retrieve entries from a csv file.
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
def get_string_input(message: str, max_length: int = MAX_NAME_LENGTH) -> str:
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
            if not string or string.isdigit() or len(string) > max_length:
                raise ValueError(f"Input Cannot be Empty, a Number, or Longer than {max_length} Characters.")
            is_valid = True
        except ValueError as e:
            print(f"Invalid Input. Please Enter a Valid String. {e}")
    return string
```

```python
def get_float_input(message: str, max_value: float = MAX_NUMERIC_VALUE) -> float:
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
            if number > max_value:
                raise ValueError(f"Input Cannot Exceed {max_value}.")
            is_valid = True
        except ValueError as e:
            print(f"Invalid Input. Please Enter a Valid Number. {e}")
    return number
```

```python
def get_int_input(message: str, max_value: int = MAX_NUMERIC_VALUE) -> int:
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
            if integer > max_value:
                raise ValueError(f"Input Cannot Exceed {int(max_value)}.")
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

Project layout:

```
Nutrition_Tracker/
├── README.md                       # Project overview & user guide
|–– requirements.txt                # Stores the required libraries
├── src/                            # Source code
│   ├── main.py                     # Entry point & main loop routing
│   ├── ui.py                       # Terminal UI & input validation
│   ├── data.py                     # Persistence + lookups + analytics
│   ├── visualization.py            # Graph generation for 7-day nutrition data
│   ├── visualization.ipynb         # Reference notebook for interactive exploration
│   └── data/                       # Data storage directory
│       └── data.csv                # Persistent nutrition entries (CSV)
```
### Architecture Overview 🧱
- **`main.py` (Flow Coordinator)**: Application entry point with module docstring. Runs the main loop, interprets user choices, dispatches operations to ui and data modules. Includes exception handling for each menu choice.
- **`ui.py` (Presentation / Interaction)**: Terminal interface with comprehensive type hints. Renders menus & tables, performs input validation with upper bounds (`MAX_NAME_LENGTH = 30`, `MAX_NUMERIC_VALUE = 10000.0`). All functions fully documented with Args/Returns/Note sections. Implements standardized error messages with "Error:" prefix and 2-second visibility.
- **`data.py` (Data & Analytics)**: Persistence layer with full type hints. Handles CSV operations with `newline=''` parameter, entry queries, daily/weekly analytics, and corruption scanning. All functions documented with comprehensive docstrings.
- **`visualization.py` (Graph Generation)**: Module for creating and saving nutrition graphs. The `create_nutrition_graph()` function fetches 7-day data, processes it with pandas, and generates a bar chart showing daily macronutrient intake. Saves output to `graphs/graph.png` with error handling for missing data.
- **`visualization.ipynb`**: Reference Jupyter notebook for interactive exploration and testing of visualization code. Maintained alongside `.py` file for reference.
- **`src/data/data.csv` (Storage)**: Flat append-only store of nutrition records with columns: Name, Protein, Fat, Carbs, Calories, DateTime. Includes sample test data for immediate feature testing.
- **`graphs/` (Output Directory)**: Stores generated nutrition graphs (e.g., `graph.png`) for 7-day visualization.
- **`main.py`**: Application entry point (now ~164 lines). Clean handler functions: `handle_add_entry()`, `handle_reuse_entry()`, `handle_view_entries()`, `handle_statistics()`, `handle_exit()`. Main loop uses handler dictionary for elegant dispatch.
- **`ui.py`**: Terminal interface with 12+ typed functions. Input validation with constants (`MAX_NAME_LENGTH: int = 30`, `MAX_NUMERIC_VALUE: float = 10000.0`), display functions for menus/tables/stats, standardized error messages with "Error:" prefix and 2-second visibility.
- **`data.py`**: Data persistence and analytics with pure computation functions. **Pure functions** (no I/O): `compute_totals()`, `compute_averages()`. **I/O wrappers**: `get_all_entries()`, `get_entries_by_date()`, `get_daily_totals()`, `get_weekly_averages()`, `scan_csv_for_corruption()`.
- **`visualization.py`**: Graph generation module with `create_nutrition_graph()` function. Fetches 7-day entries, validates data with pandas, creates grouped bar chart showing Calories/Protein/Fat/Carbs, and saves to `graphs/graph.png` with proper error handling.
- **`data.csv`**: Flat storage with append-only rows (Name, Protein, Fat, Carbs, Calories, DateTime). Includes 24 sample entries spanning 7 days for immediate testing.

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
     ┌───────┼──────────────────────────────────────────────────────────────────────────────–––─┐
     │       │                                                                                  │
     │       │ Choice == 1 (Add Entry)                                                          │
     │       │   ┌──────────────────────────────────────────────────────────────────────────┐   │
     │       │   │ ui.clear_terminal()                                                      │   │
     │       │   │ name = ui.get_string_input() (≤30 chars)                                 │   │
     │       │   │ protein = ui.get_float_input()                                           │   │
     │       │   │ fat = ui.get_float_input()                                               │   │
     │       │   │ carbs = ui.get_float_input()                                             │   │
     │       │   │ calories = ui.get_float_input()                                          │   │
     │       │   │ data.write_nutrition_data([... dt.now()])                                │   │
     │       │   │ ui.add_nutrition_successful() | ui.add_nutrition_failed(e)               │   │
     │       │   └──────────────────────────────────────────────────────────────────────────┘   │
     │       │                                                                                  │
     │       │ Choice == 2 (Reuse Existing Entry)                                               │
     │       │   ┌──────────────────────────────────────────────────────────────────────────-┐  │
     │       │   │ ui.clear_terminal()                                                       │  │
     │       │   │ recipe = ui.get_string_input()                                            │  │
     │       │   │ entry = data.get_entry_by_name(recipe)                                    │  │
     │       │   │ IF entry found:                                                           │  │
     │       │   │   data.write_nutrition_data(copy + new timestamp)                         │  │
     │       │   │   ui.add_nutrition_successful()                                           │  │
     │       │   │ ELSE: ui.add_nutrition_failed("Recipe Not Found")                         │  │
     │       │   └──────────────────────────────────────────────────────────────────────────–┘  │
     │       │                                                                                  │
     │       │ Choice == 3 (View Entries)                                                       │
     │       │   ┌──────────────────────────────────────────────────────────────────────────┐   │
     │       │   │ ui.clear_terminal()                                                      │   │
     │       │   │ entries = data.get_all_entries()                                         │   │
     │       │   │ ui.show_entries(entries, "Nutrition Entries:", "No Entries Found.")      │   │
     │       │   └──────────────────────────────────────────────────────────────────────────┘   │
     │       │                                                                                  │
     │       │ Choice == 4 (Statistics Submenu)                                                 │
     │       │   ┌─────────────────────────────────────────────────────────────────────────-─┐  │
     │       │   │ stats_running = True                                                      │  │
     │       │   │ WHILE stats_running:                                                      │  │
     │       │   │   ui.show_statistics_menu()                                               │  │
     │       │   │   stats_choice = ui.get_int_input()                                       │  │
     │       │   │   IF 1 (Daily Totals):                                                    │  │
     │       │   │     totals = data.get_daily_totals()                                      │  │
     │       │   │     ui.show_entries(totals, "Daily Total Intake", "No Entries Today")     │  │
     │       │   │     stats_running = False                                                 │  │
     │       │   │   IF 2 (Weekly Averages):                                                 │  │
     │       │   │     averages = data.get_weekly_averages()                                 │  │
     │       │   │     ui.show_entries(averages, "Weekly Average Intake", "No Entries Week") │  │
     │       │   │     stats_running = False                                                 │  │
     │       │   │   IF 3 (Create Nutrition Graph):                                          │  │
     │       │   │     visualization.create_nutrition_graph()                                │  │
     │       │   │     stats_running = False                                                 │  │
     │       │   │   IF 4 (Back to Main Menu):                                               │  │
     │       │   │     ui.clear_terminal()                                                   │  │
     │       │   │     stats_running = False                                                 │  │
     │       │   └──────────────────────────────────────────────────────────────────────────–┘  │
     │       │                                                                                  │
     │       │ Choice == 5 (Exit)                                                               │
     │       │   ┌──────────────────────────────────────────────────────────────────────────┐   │
     │       │   │ ui.exit_message()                                                        │   │
     │       │   │ is_running = False                                                       │   │
     │       │   └──────────────────────────────────────────────────────────────────────────┘   │
     │       │                                                                                  │
     │       │ ELSE (Invalid Choice) → ui.invalid_choice()                                      │
     └───────┘                                                                                  │
                         │                                                                      │
                         ▼                                                                      │
 ┌────────────────────────────┐                                                                 │
 │ is_running == False ?      │◀────────────────────────────────────────────────────────────────┘
 └────────────┬───────────────┘
              │YES
              ▼
┌────────────────────────────┐
│          EXIT              │
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


## 🧩 User Manual

The following section explains step-by-step how to use the **Nutrition Tracker** application.

---

### ️1. Start the Program 🚀

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

### 2. Add a New Food Entry ➕

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

### ️3. View All Entries 📋

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

### 4. View Entries from the Current Week 🗓️

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

### 5. Show Statistics 📊

Select option **4** from the main menu.  
A submenu will appear with three statistical options:

```
Statistics Menu:
1. Daily Totals
2. Weekly Averages
3. Create Nutrition Graph
4. Back to Main Menu
```

#### Option 1: Daily Totals 📈
Shows the total intake of Protein, Fat, Carbs, and Calories **for today**.

Example output:
```
Daily Total Intake
Name          Protein    Fat        Carbs      Calories
Daily Total   85.5g      32.2g      220.0g     1850.0 kcal
```

#### Option 2: Weekly Averages 📊
Shows the **average daily intake** over the last 7 days for Protein, Fat, Carbs, and Calories.

Example output:
```
Weekly Average Intake
Name          Protein    Fat        Carbs      Calories
Weekly Avg    62.1g      24.5g      185.3g     1420.5 kcal
```

#### Option 3: Create Nutrition Graph 📉
Generates a visual graph showing your **daily macronutrient intake for the last 7 days**.

**What happens:**
1. The program retrieves all entries from the past 7 days
2. Validates and processes the data (handles missing values gracefully)
3. Groups entries by date and sums up daily totals
4. Creates a colorful bar chart showing Calories, Protein, Fat, and Carbs per day
5. Saves the graph as `graph.png` in the `graphs/` directory
6. Displays a success message with the file path

**Example success message:**
```
Chart saved to /workspaces/Nutrition_Tracker/graphs/graph.png
```

**Viewing the graph:**
- Navigate to the `graphs/` folder in your file explorer
- Open `graph.png` to view the visualization
- The graph displays daily totals in a grouped bar chart format

**Requirements for the graph:**
- You must have **at least one entry within the last 7 days** for a graph to be generated
- All numeric values (Calories, Protein, Fat, Carbs) must be valid numbers
- Entries with missing or invalid data are automatically skipped

#### Option 4: Back to Main Menu
Returns to the main menu without generating any statistics.

➡️ Use options 1–2 to track daily/weekly intake, and option 3 to visualize trends over time.

---

### 6. Exit the Program 🚪

Select option **5** to close the program.  
All your data will be saved automatically before the application exits.

Example:
```
Exiting program...
Goodbye!
```

➡️ Always use this option to ensure your data is stored correctly before closing the program.

---

### Summary of Menu Options (Main)

| Option | Description |
|:--:|:--|
| 1 | Add a new food entry            |
| 2 | Reuse an existing entry by name |
| 3 | View all entries                |
| 4 | View statistics (submenu)       |
| 5 | Exit the program                |

### Summary of Menu Options (Statistics Submenu)

| Option | Description |
|:--:|:--|
| 1 | Show daily totals for today            |
| 2 | Show weekly average intake             |
| 3 | Create nutrition graph for last 7 days |
| 4 | Back to main menu                      |

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
- **Graph generation**: Requires `pandas`, `matplotlib` and `import-ipynb`. Run `pip install -r requirements.txt` to install.
- **Visual data analysis**: Use the graph feature to identify eating patterns and nutrition trends.

---

Enjoy tracking your meals and managing your daily calories with the **Nutrition Tracker**! 🍎

## ⚙️ Implementation

### Technology
- **Python 3.x**: Standard library only for core app, plus `pandas` and `matplotlib` for visualization
- **Type hints**: Comprehensive typing throughout with `list[dict[str, str | float]]`, etc.
- **Docstrings**: Module and function-level documentation following Google/NumPy style
- **PEP 8 compliance**: snake_case naming conventions throughout
- **Pure functions**: Computation separated from I/O for testability (`compute_totals`, `compute_averages`)
- **Handler pattern**: Menu dispatch via dictionary routing (src/main.py)

### How to Run

**1. Install Dependencies**
```bash
pip install -r requirements.txt
```

This installs:
- `pandas`: Data processing and manipulation (used in visualization)
- `matplotlib`: Graph and visualization generation
- `import-ipynb`: .ipynb file execution inside .py file 

**2. Run the Application**
```bash
python3 src/main.py
```

### Libraries Used

**Core Application:**
- `os`, `time`: UI/terminal control and pauses
- `csv`, `datetime`: File I/O and timestamps in data layer

**Visualization Module:**
- `pandas`: DataFrame operations for data processing
- `matplotlib.pyplot`: Creating and saving chart images
- `import_ipynb`: access ipynb file inside .py file

### Project Structure & Module Organization

```
src/
├── main.py              # Application entry point & main loop
├── ui.py                # Terminal UI & input validation
├── data.py              # Data persistence & analytics
├── visualization.ipynb  # Notebook version of visualization
└── data/
    └── data.csv         # Persistent CSV storage
```

**Module Responsibilities:**

| Module                | Responsibility                           | Key Functions                                                           |
|:---|:---|:---|
| `main.py`             | Application orchestration & user routing | `main()`, `handle_add_entry()`, `handle_statistics()`                   |
| `ui.py`               | Terminal interface & input validation    | `get_string_input()`, `show_main_menu()`, `show_entries()`              |
| `data.py`             | CSV persistence & analytics              | `write_nutrition_data()`, `get_daily_totals()`, `get_weekly_averages()` |
| `visualization.ipynb` | Graph generation                         | `create_nutrition_graph()`                                              |

### Importing the Visualization Module

**In `main.py`:**
```python
import import_ipynb
import visualization
```

This imports `visualization.ipynb.

**To use the graph function:**
```python
visualization.create_nutrition_graph()
```

### Dependencies & Requirements

**`requirements.txt` contains:**
```
pandas>=1.5.0
matplotlib>=3.5.0
import-ipynb>=0.1.4
```

**Install all dependencies:**
```bash
pip install -r requirements.txt
```

**Check installed packages:**
```bash
pip list | grep -E "pandas|matplotlib"
```

### Visualization Pipeline

The `create_nutrition_graph()` function:

1. **Fetch data**: Retrieves all entries from the last 7 days via `data.get_entries_within_week()`
2. **Create DataFrame**: Converts CSV rows into a pandas DataFrame for easy manipulation
3. **Validate & clean**: 
   - Converts DateTime strings to proper datetime objects
   - Converts Calories, Protein, Fat, Carbs to numeric types
   - Drops rows with missing DateTime values
   - Fills remaining NaN values with 0
4. **Group & aggregate**: Sums daily totals by date using `groupby()`
5. **Plot**: Creates a 12x6 inch grouped bar chart with:
   - X-axis: Dates from the past 7 days
   - Y-axis: Grams (for Calories, Protein, Fat, Carbs)
   - Colors: Automatic color scheme from matplotlib
   - Grid: Light horizontal grid for readability
6. **Save**: Outputs to `graphs/graph.png` in the working directory
7. **Display**: Shows success message with file path

**Error handling in visualization:**
- No entries in last 7 days → displays "No entries found" message
- All rows filtered out due to invalid data → displays "No valid entries found" message
- Graph save fails → displays error message with exception details

### Code Quality Features
- **Validation constants**: `MAX_NAME_LENGTH = 30`, `MAX_NUMERIC_VALUE = 10000.0`
- **Standardized error messages**: Consistent "Error:" prefix, 2-second visibility
- **CSV best practices**: Proper `newline=''` parameter on all file operations
- **Comprehensive type hints**: All function parameters and returns typed
- **Detailed docstrings**: Every function documented with purpose, arguments, returns, and notes
- **Handler pattern**: 6 focused functions replacing monolithic main() (110 → ~163 lines with improved readability)
- **Pure functions**: Separated computation from I/O (compute_totals, compute_averages) for 100% testability
- **Data validation in visualization**: Graceful handling of malformed data with `errors='coerce'`

## ⚠️ Known Limitations

### Data Management
- **No entry editing**: Once saved, entries cannot be modified (only new entries can be added)
- **No entry deletion**: Individual entries cannot be removed from the CSV file
- **No data backup**: Manual backup of `data.csv` required; no automatic backup mechanism
- **Single CSV file**: All data stored in one file; no database support for larger datasets
- **No data export**: Cannot export data to other formats (JSON, Excel, etc.)

### User Interface
- **Terminal-only interface**: No graphical user interface (GUI); relies entirely on console
- **Graph viewing**: Generated graphs must be manually opened from file explorer; not displayed in terminal
- **No search functionality**: Limited to search by exact name only; no advanced filtering
- **Single-user system**: No user accounts, authentication, or multi-user support
- **Platform-dependent**: Terminal clearing works differently on Windows vs Unix systems

### Functionality
- **No meal planning**: Cannot set goals or plan future meals
- **No nutritional recommendations**: No guidance on daily intake targets or health goals
- **Limited statistics**: Only daily totals and weekly averages; no monthly/yearly analysis
- **Graph requires dependencies**: Visualization feature needs pandas and matplotlib (not standard library)
- **7-day limit for graphs**: Graph generation only works with last 7 days of data
- **No time-based filtering**: Cannot view entries by specific date range (except today or last 7 days)

### Technical
- **CSV corruption handling**: Corrupted rows are skipped but not automatically fixed
- **No concurrent access protection**: Multiple instances could corrupt data if run simultaneously
- **Limited validation recovery**: Invalid data is rejected but not guided correction
- **Memory-based operations**: Entire CSV loaded into memory (may be slow with thousands of entries)

### Future Enhancement Opportunities
These limitations present opportunities for future development:
- Database integration (SQLite, PostgreSQL)
- Web-based interface with real-time graphs
- Data import/export in multiple formats
- Entry editing and deletion with audit trail
- Advanced filtering and search capabilities
- Goal setting and progress tracking

## 👥 Team & Contributions

| Name        | Contribution                                    |
|-------------|-------------------------------------------------|
| Raji        | Documentation, Main flow                        |
| Paulo       | UI functions, Main flow                         |
| Jonas       | Data functions, Main flow                       |

## About This Project
This project is intended to:
- Practice the complete process from problem analysis to implementation
- Apply basic Python programming concepts (console I/O, control flow, functions, modules)
- Demonstrate console interaction, data validation, and file processing
- Produce clean, well-structured, and documented code suitable for future teamwork
- Encourage frequent, incremental commits to track progress

## � Discussion

### Design Decisions

**Module Separation**  
We chose to separate the application into three core modules (`main.py`, `ui.py`, `data.py`) to follow the single responsibility principle. This separation made the code easier to test, debug, and maintain. Each module has a clear purpose, reducing coupling and improving readability.

**Handler Pattern**  
Instead of a monolithic `main()` function with nested if-statements, we implemented a handler pattern with dedicated functions for each menu choice. This reduced the main function from 110+ lines to ~50 lines while improving code clarity and making it easier to add new features.

**Pure Functions**  
We separated computation logic (`compute_totals()`, `compute_averages()`) from I/O operations. This design choice improved testability—pure functions can be tested without file system access—and made the analytics logic reusable across different contexts.

**CSV Over Database**  
We deliberately chose CSV for data persistence instead of a database (SQLite, etc.) to keep the project simple and aligned with the learning objectives. While this limits scalability, it demonstrates fundamental file I/O concepts and requires no external dependencies for the core application.

**Validation Constants**  
We defined `MAX_NAME_LENGTH` and `MAX_NUMERIC_VALUE` as module-level constants to ensure consistent validation across the application. This makes it easy to adjust limits globally and documents constraints clearly.

### Challenges Faced

**CSV Corruption Handling**  
Managing corrupted or malformed CSV data was more complex than anticipated. We implemented multiple safety layers: validation during write, skipping invalid rows during read, and a dedicated corruption scanner. This defensive programming ensures the app remains functional even with imperfect data.

**Cross-Platform Compatibility**  
Terminal clearing behaves differently on Windows (`cls`) vs. Unix (`clear`). We resolved this using `os.name` detection, but this highlighted the challenges of building truly portable console applications.

**Graph Display in Terminal**  
We initially hoped to display graphs directly in the terminal but discovered that matplotlib requires a GUI backend or file output. We opted to save graphs as PNG files, which works reliably but requires users to manually open the files.

### Lessons Learned

**Type Hints Are Valuable**  
Adding comprehensive type hints (`list[dict[str, str | float]]`) significantly improved our development experience. IDEs provided better autocomplete, and type errors were caught earlier during development.

**Docstrings Clarify Intent**  
Writing detailed docstrings forced us to think carefully about each function's purpose and contract. This documentation proved invaluable when team members needed to understand or modify code they didn't write.

**Input Validation Is Critical**  
We underestimated how many edge cases exist in user input. Adding upper bounds, type checking, and length limits prevented numerous potential bugs and improved the user experience by providing clear error messages.

**Incremental Development Works**  
Starting with core functionality (add entry, view entries) and gradually adding features (statistics, visualization) allowed us to maintain a working application throughout development. This incremental approach made testing easier and reduced integration problems.

### What Went Well

- **Clean Architecture**: The modular structure made collaborative development smoother
- **Comprehensive Validation**: Input checking prevented most data quality issues
- **Error Handling**: Try-except blocks and automatic CSV recreation improved reliability
- **Documentation**: Detailed README and in-code documentation made the project accessible
- **Pure Functions**: Separating computation from I/O simplified testing and debugging

### What Could Be Improved

**User Experience**
- Terminal-only interface is limiting; a GUI would be more user-friendly
- Graph generation could integrate directly into the UI instead of requiring file navigation
- More detailed error messages with correction suggestions would help users

**Data Management**
- No ability to edit or delete entries limits flexibility
- Lack of data export options (JSON, Excel) reduces interoperability
- Single CSV file doesn't scale well for large datasets

**Functionality**
- Statistics limited to daily/weekly; no monthly or yearly analysis
- No goal-setting or nutritional recommendations
- No search or filter beyond exact name matching
- Graph limited to 7 days of data

**Technical**
- No concurrent access protection could cause data corruption with simultaneous users
- Memory-based operations (loading entire CSV) may slow down with thousands of entries
- Better separation between business logic and presentation could improve testability

### Reflection on Learning Objectives

**Interactive App**: Successfully implemented a multi-level menu system with validated user input and clear feedback mechanisms.

**Data Validation**: Exceeded basic requirements with comprehensive validation including type checking, bounds validation, length limits, and CSV integrity scanning.

**File Processing**: Demonstrated proper CSV handling with `newline=''` parameter, DictReader/Writer usage, automatic file creation, and graceful error recovery.

The project successfully met all three core requirements while providing opportunities to explore advanced concepts like type hints, pure functions, and data visualization. The modular architecture and comprehensive documentation will serve as a solid foundation for future enhancements.

## 📝 License
This project is a graded group work for the programming foundation module.
