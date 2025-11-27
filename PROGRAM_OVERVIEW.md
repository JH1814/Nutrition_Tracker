# 🍎 Nutrition Tracker - Program Overview

This document provides a comprehensive explanation of how the Nutrition Tracker program works, including architecture, program flow, module interactions, and detailed feature descriptions.

---

## Table of Contents 📚
1. [Program Architecture](#program-architecture)
2. [Module Breakdown](#module-breakdown)
3. [Program Flow](#program-flow)
4. [Feature Deep Dive](#feature-deep-dive)
5. [Data Flow Diagrams](#data-flow-diagrams)
6. [Error Handling Strategy](#error-handling-strategy)
7. [User Journey Examples](#user-journey-examples)

---

## 1. Program Architecture 🧱

### 1.1 Current Implementation Structure 🧩

The program is organized pragmatically around three cooperating modules and a persistent CSV file. Instead of emphasizing a formal pattern name, the documentation below focuses on what each part actually does today:

```
┌────────────────────────────────────────────────────────────────┐
│                           main.py                              │
│  - Starts and controls the application loop                    │
│  - Routes validated user choices to concrete operations        │
│  - Coordinates retrieval, analytics, and output formatting     │
└───────────────┬───────────────────────────────────────────────┘
        │ Calls
    ┌───────▼────────┐
    │     ui.py      │
    │  - Terminal I/O│
    │  - Input loops │
    │  - Menu/table  │
    └───────┬────────┘
        │ Requests / Displays
    ┌───────▼────────┐
    │    data.py     │
    │  - File checks │
    │  - CSV read    │
    │  - Write rows  │
    │  - Analytics   │
    │  - Lookups     │
    └───────┬────────┘
        │ Persists
    ┌───────▼────────┐
    │  data/data.csv │
    │  - Flat storage│
    └────────────────┘
```

### 1.2 Rationale 💡
- Keep responsibilities clear without over‑engineering abstractions.
- Minimize indirection: analytics and persistence share one module for simplicity.
- Allow future evolution (e.g., splitting `data.py` into service + repository) without rewriting user interaction logic.

### 1.3 Potential Evolution Path (Future, Not Implemented Yet) 🔭
- Introduce a domain data class (`NutritionEntry`) for stronger typing.
- Extract persistence into a repository layer if storage changes (e.g., SQLite).
- Separate analytics into a service layer for test isolation.

### 1.4 Benefits of Current Layout ✅
- Straightforward navigation: one place for data operations.
- Low cognitive overhead for small feature additions.
- Easy recovery logic (file existence + creation in same module).
- Clear flow from user input → orchestration → data operations → output.

---

### 1.5 Module Responsibility Summary 🗂️

| Module | Responsibility Focus | Representative Functions |
|--------|----------------------|--------------------------|
| `main.py` | Application flow & routing | `main()` loop, statistics submenu handling |
| `ui.py` | Terminal interaction & validation | `showMainMenu()`, `getIntInput()`, `showEntries()` |
| `data.py` | Persistence + data logic + analytics | `checkCsvFileExists()`, `writeNutritionData()`, `getAllEntries()`, `getDailyTotals()` |
| `data/data.csv` | Flat storage medium | (Rows appended / read) |

---

## 2. Module Breakdown 🧬

### 2.1 main.py (Flow Coordinator) 🧭

**Purpose:** Entry point controlling the primary loop and dispatching actions.

**Key Components:**

```python
import data
import ui
import datetime

def main() -> None:
    is_running = True
    while is_running:
        # Main loop
        data.checkCsvFileExists()
        ui.showMainMenu()
        choice = ui.getIntInput("Enter your Choice: ")
        
        # Route to appropriate handler
        if choice == 1:
            # Add new entry
        elif choice == 2:
            # Use existing entry
        elif choice == 3:
            # View entries
        elif choice == 4:
            # Statistics submenu
        elif choice == 5:
            # Exit
        else:
            # Invalid choice
```

**Responsibilities:**
1. **Program initialization:** Start main loop
2. **Menu routing:** Direct user choices to appropriate functions
3. **Data coordination:** Call data module functions
4. **UI coordination:** Call ui module functions
5. **Error handling:** Catch and handle exceptions
6. **Program termination:** Clean exit

---

### 2.2 data.py (Data & Analytics Module) 📊

**Purpose:** Houses both low-level CSV access and higher-level nutrition calculations.

**Imports:**
```python
import csv
import datetime
import os
```

**Configuration:**
```python
csv_file_path = os.path.join(os.path.dirname(__file__), "data", "data.csv")
```

**Function Categories:**

#### File Management
- `checkCsvFileExists()` - Ensures data file exists
- `createCsvFile()` - Creates new CSV with headers
- `writeNutritionData(data)` - Appends entry to CSV

#### Data Retrieval
- `getAllEntries()` - Returns all valid entries
- `getEntriesByDate(date)` - Returns entries for specific date
- `getEntriesWithinWeek()` - Returns last 7 days of entries
- `getEntryByName(name)` - Finds entry by exact name match

#### Data Quality
- `scanCsvForCorruption()` - Counts corrupted rows

#### Analytics
- `getDailyTotals()` - Sums nutrition for today
- `getWeeklyAverages()` - Averages nutrition over week

---

### 2.3 ui.py (Terminal Interaction Module) 🖥️

**Purpose:** Encapsulates user input loops, menu rendering, tabular output, and messaging.

**Imports:**
```python
import os
import time
```

**Function Categories:**

#### Display Functions
- `showMainMenu()` - Displays main menu
- `showStatisticsMenu()` - Displays statistics submenu
- `showEntries(entries, message)` - Displays entry table
- `showEntriesFailed(error)` - Shows error message

#### Success/Failure Messages
- `addNutritionSuccessful()` - Success confirmation
- `addNutritionFailed(error)` - Failure notification
- `invalidChoice()` - Invalid input warning
- `exitMessage()` - Goodbye message

#### Input Functions
- `getStringInput(message)` - Validates and returns string
- `getFloatInput(message)` - Validates and returns float
- `getIntInput(message)` - Validates and returns integer

#### Utility Functions
- `clearTerminal()` - Clears console (cross-platform)

---

## 3. Program Flow 🔀

### 3.1 Application Lifecycle ♻️

```
START
  │
  ▼
┌─────────────────────────┐
│  if __name__ == "__main__" │
│       main()               │
└───────────┬────────────────┘
            │
            ▼
    ┌───────────────┐
    │ is_running = True │
    └───────┬───────────┘
            │
    ┌───────▼──────────────────┐
    │   MAIN LOOP (while)      │
    │                           │
    │  1. checkCsvFileExists()  │
    │  2. showMainMenu()        │
    │  3. Get user choice       │
    │  4. Execute action        │
    │  5. Loop or exit          │
    └───────┬──────────────────┘
            │
    ┌───────▼───────┐
    │ is_running =  │
    │    False?     │
    └───┬───────┬───┘
        │       │
       YES     NO
        │       │
        ▼       └──┐
      EXIT         │
                   └──▶ Continue Loop
```

---

### 3.2 Main Loop Detailed 🔎

**Step-by-step execution:**

```python
def main() -> None:
    is_running = True
    while is_running:  # Infinite loop until user exits
        
        # STEP 1: Ensure data file exists
        data.checkCsvFileExists()
        
        # STEP 2: Display menu
        ui.showMainMenu()
        
        # STEP 3: Get validated user choice
        choice = ui.getIntInput("Enter your Choice: ")
        
        # STEP 4: Route based on choice
        if choice == 1:
            # Handler: Add new nutrition entry
        elif choice == 2:
            # Handler: Use existing entry (reuse recipe)
        elif choice == 3:
            # Handler: View all entries
        elif choice == 4:
            # Handler: Statistics submenu
        elif choice == 5:
            # Handler: Exit program
            is_running = False
        else:
            # Handler: Invalid choice
```

---

## 4. Feature Deep Dive 🥽

### 4.1 Feature 1: Add Nutrition Entry ➕

**User Action:** Select option 1 from main menu

**Complete Flow:**

```python
# STEP 1: Clear screen and prompt for inputs
ui.clearTerminal()
name = ui.getStringInput("Add Name of Nutrition Entry: ")
protein = ui.getFloatInput("Add Protein in grams: ")
fat = ui.getFloatInput("Add Fat in grams: ")
carbs = ui.getFloatInput("Add Carbs in grams: ")
calories = ui.getFloatInput("Add Calories in kcal: ")

# STEP 2: Attempt to write data
try:
    data.checkCsvFileExists()  # Verify file exists
    # Write entry with current timestamp
    data.writeNutritionData([
        name, protein, fat, carbs, calories, 
        datetime.datetime.now()
    ])
    ui.addNutritionSuccessfull()  # Show success message
    
# STEP 3: Handle errors
except FileNotFoundError as e:
    data.createCsvFile()  # Recreate if missing
    ui.addNutritionFailed(e)  # Show failure message
```

**Interaction Diagram:**
```
User Input (via ui.py)
    ↓
Validation (ui.getStringInput, ui.getFloatInput)
    ↓
Controller (main.py) collects inputs
    ↓
Model (data.writeNutritionData)
    ↓
CSV File (append operation)
    ↓
View (ui.addNutritionSuccessfull)
    ↓
Back to Main Menu
```

**Example Session:**
```
Add Name of Nutrition Entry: Chicken Salad
Add Protein in grams: 35
Add Fat in grams: 12
Add Carbs in grams: 25
Add Calories in kcal: 350

Nutrition Data Added Successfully!
```

**Result in CSV:**
```csv
Chicken Salad,35,12,25,350,2025-11-27 14:30:15.123456
```

---

### 4.2 Feature 2: Use Existing Nutrition Entry ♻️

**User Action:** Select option 2 from main menu

**Purpose:** Reuse a previous entry's nutrition values with a new timestamp

**Complete Flow:**

```python
# STEP 1: Get recipe name from user
ui.clearTerminal()
recipe = ui.getStringInput("Enter the Name of the Recipe: ")

# STEP 2: Search for entry
entry = []
try:
    entry = data.getEntryByName(recipe)
except FileNotFoundError as e:
    data.createCsvFile()
    ui.addNutritionFailed(e)
except ValueError as e:
    ui.addNutritionFailed(e)

# STEP 3: Write if found
if entry:
    try:
        data.checkCsvFileExists()
        # Reuse nutrition values, new timestamp
        data.writeNutritionData((
            entry[0]["Name"],
            entry[0]["Protein"],
            entry[0]["Fat"],
            entry[0]["Carbs"],
            entry[0]["Calories"],
            datetime.datetime.now()  # NEW timestamp
        ))
        ui.addNutritionSuccessfull()
    except FileNotFoundError as e:
        data.createCsvFile()
        ui.addNutritionFailed(e)
else:
    ui.addNutritionFailed("Recipe Not Found")
```

**Why This Feature Matters:**
- Quickly log recurring meals
- Ensures consistency (same nutrition values)
- Saves time (no re-entry)

**Example Session:**
```
Enter the Name of the Recipe: Pizza

Nutrition Data Added Successfully!
```

**Result:** New row added with Pizza's values and current timestamp

---

### 4.3 Feature 3: View Nutrition Entries 📋

**User Action:** Select option 3 from main menu

**Complete Flow:**

```python
ui.clearTerminal()
try:
    # STEP 1: Retrieve all valid entries
    entries = data.getAllEntries()

    # STEP 2: Centralized display + single corruption warning
    ui.showStatsResult(entries, "Nutrition Entries:", "No Entries Found.")

except FileNotFoundError as e:
    data.createCsvFile()
    ui.showEntriesFailed(e)
except IndexError as e:
    ui.showEntriesFailed(e)
```

**Display Format:**

```
Nutrition Entries:
Name                           Protein    Fat        Carbs      Calories  
--------------------------------------------------------------------------------
Chicken Salad                  35g        12g        25g        350 kcal  
Pizza                          30g        7.5g       200g       600 kcal  
Burger                         20g        5g         500g       500 kcal  

Press Enter to continue...
```

**Behind the Scenes:**

1. `data.getAllEntries()` reads CSV, skips corrupted rows
2. `ui.showEntries()` formats data as table
3. `data.scanCsvForCorruption()` counts bad rows
4. Warning displayed if corruption found

---

### 4.4 Feature 4: View Statistics 📊

**User Action:** Select option 4 from main menu

**Submenu Structure:**

```python
stats_running = True
while stats_running:
    ui.showStatisticsMenu()
    stats_choice = ui.getIntInput("Select Statistics Type: ")
    
    if stats_choice == 1:
        # Daily Totals
    elif stats_choice == 2:
        # Weekly Averages
    elif stats_choice == 3:
        # Back to main menu
        stats_running = False
```

---

#### 4.4.1 Daily Totals (Stats Option 1)

**Purpose:** Sum all nutrition values for today

**Implementation:**

```python
totals = data.getDailyTotals()
if totals:
    ui.showEntries(totals, "Daily Total Intake")
    # Check corruption
    corrupt_count = data.scanCsvForCorruption()
    if corrupt_count > 0:
        ui.showEntriesFailed(f"Warning: {corrupt_count} corrupted row(s)")
else:
    ui.showEntriesFailed("No Entries Found for Today")
```

**Calculation Logic (in data.py):**

```python
def getDailyTotals() -> list[dict]:
    # Get today's entries
    entries = getEntriesByDate()
    
    if not entries:
        return None
    
    # Initialize counters
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
    
    # Return as list with single dict (for UI compatibility)
    return [{
        'Protein': round(total_protein, 2),
        'Fat': round(total_fat, 2),
        'Carbs': round(total_carbs, 2),
        'Calories': round(total_calories, 2)
    }]
```

**Example Output:**
```
Daily Total Intake:
Name                           Protein    Fat        Carbs      Calories  
--------------------------------------------------------------------------------
                               85.0g      29.5g      225.0g     1450 kcal 

Press Enter to continue...
```

---

#### 4.4.2 Weekly Averages (Stats Option 2)

**Purpose:** Calculate average nutrition per day over last 7 days

**Implementation:**

```python
averages = data.getWeeklyAverages()
if averages:
    ui.showEntries(averages, "Weekly Average Intake")
else:
    ui.showEntriesFailed("No Entries Found for this Week")
```

**Calculation Logic (in data.py):**

```python
def getWeeklyAverages() -> list[dict]:
    # Get last 7 days of entries
    entries = getEntriesWithinWeek()
    
    if not entries:
        return None
    
    # Initialize counters
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
            pass
    
    # Calculate averages
    count = len(entries)
    return [{
        'Protein': round(total_protein / count, 2),
        'Fat': round(total_fat / count, 2),
        'Carbs': round(total_carbs / count, 2),
        'Calories': round(total_calories / count, 2)
    }]
```

**Key Difference from Daily Totals:**
- Divides by `count` (number of entries)
- Uses entries from last 7 days, not just today

**Example Output:**
```
Weekly Average Intake:
Name                           Protein    Fat        Carbs      Calories  
--------------------------------------------------------------------------------
                               28.3g      12.1g      98.5g      386.7 kcal

Press Enter to continue...
```

---

### 4.5 Feature 5: Exit Program 🚪

**User Action:** Select option 5 from main menu

**Implementation:**

```python
elif choice == 5:
    is_running = False  # Break main loop
    ui.exitMessage()    # Display goodbye
    break               # Explicit loop exit
```

**Exit Message Function:**

```python
def exitMessage() -> None:
    clearTerminal()
    print("Exiting the Nutrition Tracker. Goodbye!")
    time.sleep(2)
    clearTerminal()
```

**What Happens:**
1. `is_running` set to `False` (loop condition fails)
2. Goodbye message displayed for 2 seconds
3. Screen cleared
4. Program terminates

---

## 5. Data Flow Diagrams 🧭

### 5.1 Input Validation Flow ✅

```
User Types Input
       │
       ▼
┌──────────────────┐
│  ui.getXInput()  │  (X = String, Float, or Int)
└────────┬─────────┘
         │
    ┌────▼────┐
    │  Valid? │
    └──┬───┬──┘
       │   │
      YES  NO
       │   │
       │   └──▶ Print Error
       │             │
       │             └──▶ Loop (re-prompt)
       │
       ▼
  Return Value
       │
       ▼
  main.py uses value
```

**Example: String Input Validation**

```python
def getStringInput(message: str) -> str:
    is_valid = False
    while not is_valid:
        try:
            string = input(message)
            if not string or string.isdigit():
                raise ValueError("Input Cannot be Empty or a Number.")
            is_valid = True
        except ValueError as e:
            print(f"Invalid Input. Please Enter a Valid String. {e}")
    return string
```

---

### 5.2 Data Retrieval Flow 📥

```
main.py calls data function
       │
       ▼
┌──────────────────────┐
│ data.getAllEntries() │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│  Open CSV file       │
│  (csv.DictReader)    │
└──────────┬───────────┘
           │
           ▼
    ┌──────────────┐
    │  For each row│
    └──────┬───────┘
           │
    ┌──────▼────────┐
    │  Validate row │
    │  (Name field) │
    └──────┬────────┘
           │
    ┌──────▼────────┐
    │  Valid?       │
    └───┬───────┬───┘
        │       │
       YES     NO
        │       │
        │       └──▶ Skip (continue)
        │
        ▼
   Append to list
        │
        ▼
  Return list to main.py
        │
        ▼
  main.py passes to ui.showEntries()
```

---

### 5.3 Write Data Flow 📤

```
User inputs values
       │
       ▼
main.py collects inputs
       │
       ▼
data.writeNutritionData([values])
       │
       ▼
┌──────────────────────┐
│  Open CSV file       │
│  (append mode 'a')   │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│  csv.writer()        │
│  .writerow(values)   │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│  File auto-closed    │
│  (context manager)   │
└──────────┬───────────┘
           │
           ▼
   Data persisted to disk
```

---

## 6. Error Handling Strategy 🧯

### 6.1 Layered Error Handling

The program uses **defensive programming** with multiple error handling layers:

#### Layer 1: Input Validation (Preventive)
- UI functions validate before returning
- Loops until valid input received
- Prevents bad data from entering system

```python
def getFloatInput(message: str) -> float:
    is_valid = False
    while not is_valid:
        try:
            number = float(input(message))
            is_valid = True
        except ValueError as e:
            print(f"Invalid Input. Please Enter a Valid Number. {e}")
    return number
```

#### Layer 2: Data Validation (Resilient)
- Data functions skip corrupted rows
- Continue processing valid data
- Don't crash on malformed input

```python
for row in reader:
    if not row.get('Name', '').strip():
        continue  # Skip, don't crash
```

#### Layer 3: Exception Handling (Recovery)
- Try-except blocks in main.py
- Auto-recovery (recreate files)
- User-friendly error messages

```python
try:
    data.writeNutritionData(...)
    ui.addNutritionSuccessfull()
except FileNotFoundError as e:
    data.createCsvFile()  # Auto-recovery
    ui.addNutritionFailed(e)
```

---

### 6.2 Common Error Scenarios

| Error | Cause | Handling | Recovery |
|-------|-------|----------|----------|
| Empty string input | User presses Enter without typing | `getStringInput()` loops | Re-prompt user |
| Invalid number | User types text for numeric field | `getFloatInput()` catches `ValueError` | Re-prompt user |
| File not found | CSV deleted while running | Catch `FileNotFoundError` | Call `createCsvFile()` |
| Corrupted CSV row | Manual edit, empty name | Skip row in read functions | Show warning, process valid rows |
| Invalid DateTime | Malformed timestamp | Catch in try-except | Skip row, continue |

---

## 7. User Journey Examples 🧗

### 7.1 Journey: First-Time User

**Scenario:** User runs program for the first time (no data file exists)

```
Step 1: Program starts
  → main() called
  → data.checkCsvFileExists() called
  → File doesn't exist
  → data.createCsvFile() creates CSV with headers

Step 2: Main menu displayed
  Welcome to the Nutrition Tracker!
  1. Add Nutrition Entry
  2. Use Existing Nutrition Entry
  3. View Nutrition Entries
  4. View Statistics
  5. Exit

Step 3: User selects 1 (Add Entry)
  Add Name of Nutrition Entry: Oatmeal
  Add Protein in grams: 6
  Add Fat in grams: 4
  Add Carbs in grams: 45
  Add Calories in kcal: 240
  
  → Validation passes
  → Data written to CSV
  → Success message displayed

Step 4: Back to main menu
  → Loop continues
```

---

### 7.2 Journey: Daily Tracking

**Scenario:** User logs meals throughout the day

```
Morning (8 AM):
  Option 1 → Add Entry: "Oatmeal with Berries"
  
Lunch (12 PM):
  Option 1 → Add Entry: "Chicken Salad"
  
Snack (3 PM):
  Option 2 → Use Existing: "Protein Shake" (from yesterday)
  
Dinner (7 PM):
  Option 1 → Add Entry: "Grilled Salmon"
  
Evening (9 PM):
  Option 4 → View Statistics
    Option 1 → Daily Totals
    (Shows sum of all today's entries)
```

---

### 7.3 Journey: Weekly Review

**Scenario:** User reviews weekly nutrition trends

```
Step 1: Option 4 (Statistics)

Step 2: Option 2 (Weekly Averages)
  → data.getEntriesWithinWeek() retrieves last 7 days
  → data.getWeeklyAverages() calculates averages
  → ui.showEntries() displays results
  
Output:
  Weekly Average Intake:
  Protein: 28.3g
  Fat: 12.1g
  Carbs: 98.5g
  Calories: 386.7 kcal
  
Step 3: Press Enter to continue

Step 4: Option 3 (Back to Main Menu)
```

---

### 7.4 Journey: Error Recovery

**Scenario:** User accidentally deletes CSV file while program running

```
Step 1: User selects 1 (Add Entry)

Step 2: User fills in details
  Name: Pizza
  Protein: 30
  ...

Step 3: Meanwhile, user deletes ./data/data.csv

Step 4: Program attempts writeNutritionData()
  → FileNotFoundError raised
  → Exception caught in main.py
  → data.createCsvFile() called
  → New file created with headers
  → User sees: "Failed to Add Nutrition Data: [error]"

Step 5: User tries again (Option 1)
  → File now exists
  → Data written successfully
```

**Key Point:** Program recovers automatically, doesn't crash

---

## 8. Key Design Decisions 🧠

### 8.1 Why CSV? 🗃️

**Advantages:**
- ✅ Human-readable (can edit in Excel/text editor)
- ✅ Simple to implement (built-in csv module)
- ✅ No database setup required
- ✅ Portable (single file)
- ✅ Version control friendly

**Tradeoffs:**
- ❌ No concurrent access protection
- ❌ Full file scans for queries
- ❌ No relational data
- ❌ Manual corruption possible

---

### 8.2 Why DictReader? 🧾

**Alternative:** `csv.reader()` returns lists

```python
# With csv.reader (list-based)
row = ['Pizza', '30', '7.5', '200', '600', '2025-11-27...']
protein = row[1]  # Positional access (fragile)

# With csv.DictReader (dict-based)
row = {'Name': 'Pizza', 'Protein': '30', ...}
protein = row['Protein']  # Named access (clear)
```

**Benefits:**
- Self-documenting code
- Resilient to column order changes
- Safe dictionary access with `.get()`

---

### 8.3 Why Append Mode? ➕

```python
with open(csv_file_path, "a") as file:  # 'a' = append
```

**Reasoning:**
- Preserves existing data
- Fast (no read-modify-write)
- Simple (no in-memory data structure)
- Safe (file pointer at end)

**Alternative (update mode):** Would require reading entire file, modifying in memory, rewriting—much slower and riskier

---

### 8.4 Why Skip vs. Raise? ⏭️

**Pattern:**
```python
if not row.get('Name', '').strip():
    continue  # Skip bad row
    # Alternative: raise ValueError("Bad row!")
```

**Decision:** Skip corrupted rows, continue processing

**Reasoning:**
- One bad row shouldn't crash entire operation
- Valid data is still valuable
- Corruption count reported separately
- Better user experience

---

## 9. Program State ⚙️

### 9.1 Stateless Design 🧼

**Key characteristic:** Program does **not** maintain state between operations

```python
# No global state
entries = data.getAllEntries()  # Reads file fresh each time
```

**Implications:**
- File is source of truth
- No synchronization issues
- Simple reasoning about program
- Potentially inefficient (re-reads file)

---

### 9.2 Session Variables 🧮

Only two persistent variables across loop iterations:

```python
def main() -> None:
    is_running = True  # Controls main loop
    while is_running:
        # ...
        if choice == 5:
            is_running = False  # Exit condition
```

And within statistics submenu:

```python
stats_running = True  # Controls stats loop
while stats_running:
    # ...
    if stats_choice == 3:
        stats_running = False  # Exit submenu
```

---

## 10. Performance Characteristics 🚀

### 10.1 Operation Costs

| User Action | File Opens | Full File Reads | Time Complexity |
|-------------|-----------|-----------------|-----------------|
| Add entry | 1 | 0 | O(1) |
| View entries | 2 | 2 | O(n) |
| Daily totals | 3 | 3 | O(n) |
| Weekly averages | 3 | 3 | O(n) |

Where n = number of rows in CSV

---

### 10.2 Optimization Opportunities

**Current:** Each operation reads file independently

```python
# View entries (Option 3)
entries = data.getAllEntries()        # Read 1
corrupt = data.scanCsvForCorruption() # Read 2
```

**Potential improvement:** Cache file in memory after first read

```python
# Hypothetical cached version
cache = load_once()
entries = filter_valid(cache)
corrupt = count_corrupted(cache)
```

**Tradeoff:** Complexity vs. performance (current design favors simplicity)

---

## Summary

The Nutrition Tracker is a **console-based nutrition logging application** that:

1. **Stores** nutrition data in CSV format
2. **Validates** user input rigorously
3. **Handles** errors gracefully with auto-recovery
4. **Provides** CRUD operations (Create, Read, no Update/Delete)
5. **Calculates** daily totals and weekly averages
6. **Maintains** data integrity through defensive programming

**Architecture strengths:**
- Clear module boundaries (flow vs. I/O vs. data logic)
- Defensive error handling (validation + graceful degradation)
- User-friendly messaging and input sanitation
- Data resilience (skip corrupted rows, warn instead of fail)

**Design philosophy:**
- Simplicity over premature abstraction
- Robustness and recoverability over feature breadth
- Clear user experience and transparency in data handling

---

**Last Updated:** November 27, 2025
