# 📄 File Processing Documentation

This document describes how the Nutrition Tracker application reads, writes, and manages CSV data files. The current implementation is module-oriented without enforcing a formal layered pattern: `main.py` coordinates flow, `data.py` performs all CSV persistence and analytics, and `ui.py` handles terminal interaction. The focus here is strictly on file handling behavior.

---

## Table of Contents 📚
1. [Overview](#overview)
2. [File Structure](#file-structure)
3. [File Initialization](#file-initialization)
4. [Writing Data to CSV](#writing-data-to-csv)
5. [Reading Data from CSV](#reading-data-from-csv)
6. [Data Filtering and Queries](#data-filtering-and-queries)
7. [File Processing Patterns](#file-processing-patterns)
8. [Performance Characteristics](#performance-characteristics)

---

## 1. Overview 🧭

### File Processing Architecture 🧱

The Nutrition Tracker uses **CSV (Comma-Separated Values)** format for data persistence. The CSV path is resolved relative to the `data.py` module for stability:

```
csv_file_path = os.path.join(os.path.dirname(__file__), "data", "data.csv")
```

**Key Design Decisions:**
- **Format:** CSV (human-readable, easy to edit manually)
- **Library:** Python's built-in `csv` module
- **Access Pattern:** File opened/closed for each operation (no persistent file handles)
- **Reading Strategy:** Uses `csv.DictReader` for row-as-dictionary access
- **Writing Strategy:** Uses `csv.writer` with append mode

---

## 2. File Structure 🗂️

### 2.1 CSV Schema 🧾

The data file has a fixed column structure defined during file creation:

```csv
Name,Protein,Fat,Carbs,Calories,DateTime
```

**Column Definitions:**

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| `Name` | String | Food/recipe name | `"Chicken Salad"` |
| `Protein` | Float | Protein content in grams | `35` |
| `Fat` | Float | Fat content in grams | `12` |
| `Carbs` | Float | Carbohydrate content in grams | `25` |
| `Calories` | Float | Caloric content in kcal | `350` |
| `DateTime` | ISO 8601 String | Timestamp of entry | `2025-11-06 08:30:15.123456` |

### 2.2 Sample Data 🍽️

```csv
Name,Protein,Fat,Carbs,Calories,DateTime
Burger,20,5,500,500,2025-11-07 17:06:23.771959
Pizza,30,7.5,200,600,2025-11-07 12:06:23.771959
Chicken Salad,35,12,25,350,2025-11-06 08:30:15.123456
```

**Note:** The first row (header) defines the column names used by `csv.DictReader` to map values to dictionary keys.

---

## 3. File Initialization 🛠️

### 3.1 File Path Configuration 📍

The CSV file path is defined as a module-level constant:

```python
# In data.py
import csv
import datetime

csv_file_path = "./data/data.csv"
```

**Path Details:**
- **Module-relative path:** Stable regardless of current working directory
- **Directory:** `./src/data/` (auto-created if missing)
- **Filename:** `data.csv`

---

### 3.2 File Creation ➕

**Function:** `create_csv_file() -> None`

**Purpose:** Creates a new CSV file with proper column headers

**Implementation:**
```python
def create_csv_file() -> None:
    os.makedirs(os.path.dirname(csv_file_path), exist_ok=True)
    with open(csv_file_path, "w") as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Protein", "Fat", "Carbs", "Calories", "DateTime"])
```

**How it works:**
1. Opens file in **write mode** (`"w"`)
   - Creates new file if it doesn't exist
   - **Overwrites** existing file if present
2. Creates a `csv.writer` object
3. Writes a single row containing column headers
4. File is automatically closed when exiting the `with` block

**When called:**
- Automatically by `check_csv_file_exists()` if file is missing
- During error recovery in main application

**Important:** This function overwrites existing data if the file already exists. In normal flow it is only called when the file is confirmed missing.

---

### 3.3 File Existence Check ✅

**Function:** `check_csv_file_exists() -> None`

**Purpose:** Ensures CSV file exists before any read/write operation

**Implementation:**
```python
def check_csv_file_exists() -> None:
    exists = False
    while not exists:
        try:
            with open(csv_file_path, "r") as file:
                exists = True
        except FileNotFoundError:
            create_csv_file()
```

**How it works:**
1. Attempts to open file in **read mode** (`"r"`)
2. If successful:
   - Sets `exists = True`
   - Exits loop
   - File handle automatically closed
3. If `FileNotFoundError` is raised:
   - Calls `create_csv_file()` to create file with headers
   - Loops again to verify creation succeeded

**Safety mechanism:**
- Loops until file exists and is readable
- Automatically recovers from missing file
- Non-invasive: only opens for reading, doesn't modify

**Called from:**
- Beginning of `main()` loop
- Before adding new entries
- During error recovery

---

## 4. Writing Data to CSV ✍️

### 4.1 Append Operation ➕

**Function:** `write_nutrition_data(data: list) -> None`

**Purpose:** Appends a new nutrition entry to the CSV file

**Implementation:**
```python
def write_nutrition_data(data: list) -> None:
    with open(csv_file_path, "a") as file:
        writer = csv.writer(file)
        writer.writerow(data)
```

**How it works:**
1. Opens file in **append mode** (`"a"`)
   - Positions file pointer at end
   - Preserves existing data
   - Creates file if missing (though should exist via `check_csv_file_exists()`)
2. Creates a `csv.writer` object
3. Writes `data` as a single row
4. Automatically closes file on exit

**Data format expected:**
```python
data = [name, protein, fat, carbs, calories, datetime_obj]
# Example:
data = ["Pizza", 30, 7.5, 200, 600, datetime.datetime.now()]
```

---

### 4.2 Writing Flow (Option 1: Add New Entry) ➕

**From `main.py`:**
```python
# User inputs values through UI
name = ui.get_string_input("Add Name of Nutrition Entry: ")
protein = ui.get_float_input("Add Protein in grams: ")
fat = ui.get_float_input("Add Fat in grams: ")
carbs = ui.get_float_input("Add Carbs in grams: ")
calories = ui.get_float_input("Add Calories in kcal: ")

try:
    data.check_csv_file_exists()  # Ensure file exists
    # Write with current timestamp
    data.write_nutrition_data([name, protein, fat, carbs, calories, datetime.datetime.now()])
    ui.add_nutrition_successful()
except FileNotFoundError as e:
    data.create_csv_file()
    ui.add_nutrition_failed(e)
```

**Process flow:**
1. Collect user input (validated by UI functions)
2. Verify file exists
3. Append data with current timestamp
4. Show success message
5. Handle exceptions if file operations fail

---

### 4.3 Writing Flow (Option 2: Reuse Existing Entry) ♻️

**From `main.py`:**
```python
recipe = ui.get_string_input("Enter the Name of the Recipe to use: ")
entry = data.get_entry_by_name(recipe)

if entry:
    try:
        # Write existing entry with NEW timestamp
        data.write_nutrition_data((
            entry[0]["Name"], 
            entry[0]["Protein"], 
            entry[0]["Fat"], 
            entry[0]["Carbs"], 
            entry[0]["Calories"], 
            datetime.datetime.now()  # New timestamp
        ))
        ui.add_nutrition_successful()
    except FileNotFoundError as e:
        data.create_csv_file()
        ui.add_nutrition_failed(e)
```

**Key difference:**
- Retrieves existing entry by name
- Creates **new row** with same nutrition values
- Uses **current timestamp** (not original entry's timestamp)
- Useful for logging recurring meals

---

## 5. Reading Data from CSV 📖

### 5.1 Basic Read Pattern 📚

All read functions follow this pattern:

```python
def readFunction() -> list:
    entries = []
    with open(csv_file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Validation and filtering logic
            entries.append(row)
    return entries
```

**Key components:**
1. **File opened in read mode** (`'r'`)
2. **`csv.DictReader` usage:**
   - Automatically reads header row
   - Converts each subsequent row to a dictionary
   - Keys = column names, Values = cell values
3. **Context manager (`with`):**
   - Ensures file is properly closed
   - Handles cleanup even if exception occurs

---

### 5.2 DictReader Row Format 🧾

When `csv.DictReader` reads a row, it creates a dictionary:

```python
# CSV row:
# Chicken Salad,35,12,25,350,2025-11-06 08:30:15.123456

# Becomes dictionary:
row = {
    'Name': 'Chicken Salad',
    'Protein': '35',
    'Fat': '12',
    'Carbs': '25',
    'Calories': '350',
    'DateTime': '2025-11-06 08:30:15.123456'
}
```

**Important:** All values are strings initially (must convert for numeric operations)

---

### 5.3 Get All Entries 📋

**Function:** `get_all_entries() -> list`

**Purpose:** Retrieve all valid entries from CSV (skips corrupted rows)

**Implementation:**
```python
def get_all_entries() -> list:
    entries = []
    with open(csv_file_path,'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Skip rows with empty name field (corrupted data)
            if not row.get('Name', '').strip():
                continue
            entries.append(row)
    return entries
```

**Processing steps:**
1. Open file for reading
2. Create DictReader (uses header for keys)
3. Iterate through each row
4. Validate Name field (skip if empty/whitespace)
5. Append valid rows to list
6. Return all valid entries

**Returns:** List of dictionaries, each representing a valid entry

**Example return value:**
```python
[
    {'Name': 'Burger', 'Protein': '20', 'Fat': '5', 'Carbs': '500', 'Calories': '500', 'DateTime': '2025-11-07 17:06:23.771959'},
    {'Name': 'Pizza', 'Protein': '30', 'Fat': '7.5', 'Carbs': '200', 'Calories': '600', 'DateTime': '2025-11-07 12:06:23.771959'},
    # ... more entries
]
```

---

## 6. Data Filtering and Queries 🔎

### 6.1 Get Entries by Date 📅

**Function:** `getEntriesByDate(date: datetime.date = datetime.datetime.now().date()) -> list`

**Purpose:** Retrieve all entries from a specific date

**Implementation:**
```python
def getEntriesByDate(date: datetime.date = datetime.datetime.now().date()) -> list:
    entries = []
    
    with open(csv_file_path,'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                # Skip rows with empty name or invalid data
                if not row.get('Name', '').strip():
                    continue
                # Parse DateTime and compare date portion
                entry_date = datetime.datetime.fromisoformat(row['DateTime']).date()
                if entry_date == date:
                    entries.append(row)
            except (ValueError, KeyError):
                # Skip entries with invalid datetime format or missing fields
                continue
    
    return entries
```

**Processing steps:**
1. Open file and create DictReader
2. For each row:
   - Validate Name field
   - Parse DateTime string to datetime object using `fromisoformat()`
   - Extract date portion with `.date()`
   - Compare with target date
   - Append if match
3. Handle exceptions (invalid datetime, missing field)
4. Return matching entries

**Default behavior:** If no date provided, uses today's date

**Example usage:**
```python
# Get today's entries
today_entries = getEntriesByDate()

# Get specific date entries
specific_date = datetime.date(2025, 11, 6)
entries = getEntriesByDate(specific_date)
```

---

### 6.2 Get Entries Within Week 🗓️

**Function:** `getEntriesWithinWeek() -> list[dict]`

**Purpose:** Retrieve all entries from the last 7 days

**Implementation:**
```python
def getEntriesWithinWeek() -> list[dict]:
    entries = []
    one_week_ago = datetime.datetime.now() - datetime.timedelta(days=7)
    
    with open(csv_file_path,'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                # Skip rows with empty name or invalid data
                if not row.get('Name', '').strip():
                    continue
                # Parse full DateTime (not just date)
                entry_date = datetime.datetime.fromisoformat(row['DateTime'])
                if entry_date >= one_week_ago:
                    entries.append(row)
            except (ValueError, KeyError):
                # Skip entries with invalid datetime format or missing fields
                continue
    
    return entries
```

**Processing steps:**
1. Calculate cutoff datetime (now - 7 days)
2. Open file and iterate rows
3. For each row:
   - Validate Name
   - Parse full DateTime (includes time component)
   - Compare with cutoff using `>=`
   - Append if within range
4. Handle parsing exceptions
5. Return all entries from last 7 days

**Key difference from `getEntriesByDate`:**
- Compares full datetime (not just date)
- Uses range comparison (`>=`) instead of equality
- Includes entries from current moment back 7 days

---

### 6.3 Get Entry by Name 🔤

**Function:** `get_entry_by_name(name: str) -> list[dict]`

**Purpose:** Find the first entry matching a specific name

**Implementation:**
```python
def get_entry_by_name(name: str) -> list[dict]:
    entry = []
    with open(csv_file_path,'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Skip rows with empty name field
            if not row.get('Name', '').strip():
                continue
            if row['Name'] == name:
                entry.append(row)
                break  # Stop after first match
    
    return entry
```

**Processing steps:**
1. Open file and iterate rows
2. Skip corrupted rows (empty Name)
3. Compare Name field with search string (exact match)
4. On match:
   - Append to result list
   - **Break** immediately (only returns first match)
5. Return list containing one entry (or empty if not found)

**Return format:**
- Success: `[{...}]` - List with one dictionary
- Not found: `[]` - Empty list

**Case sensitivity:** Exact match required (`"Pizza"` ≠ `"pizza"`)

---

### 6.4 Corruption Scanning ⚠️

**Function:** `scan_csv_for_corruption() -> int`

**Purpose:** Count corrupted rows without modifying data

**Implementation:**
```python
def scan_csv_for_corruption() -> int:
    corrupt_count = 0
    with open(csv_file_path,'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Check for empty/missing name
            if not row.get('Name', '').strip():
                corrupt_count += 1
                continue
            # Check for invalid DateTime
            try:
                _ = datetime.datetime.fromisoformat(row['DateTime'])
            except Exception:
                corrupt_count += 1
                continue
    return corrupt_count
```

**What it does:**
1. Opens file in read-only mode
2. Iterates through all rows
3. Counts rows that fail validation:
   - Empty/missing Name field
   - Invalid DateTime format
4. Does **not** collect or return the rows themselves
5. Returns integer count

**Use case:** Alert user to data quality issues while still displaying valid entries

---

## 7. File Processing Patterns 🧩

### 7.1 Open-Process-Close Pattern 🔐

**Every file operation follows this pattern:**

```python
with open(csv_file_path, mode) as file:
    # Create reader or writer
    # Process data
    # File automatically closed on exit
```

**Advantages:**
- **Automatic cleanup:** File closed even if exception occurs
- **Resource management:** No file handle leaks
- **Safety:** Ensures data is flushed to disk

---

### 7.2 Multiple Sequential Opens 🔁

**Current architecture:** File is opened and closed for each operation

```python
# Operation 1: Check existence
check_csv_file_exists()  # Opens file in 'r' mode

# Operation 2: Read data
entries = get_all_entries()  # Opens file in 'r' mode again

# Operation 3: Scan corruption
corrupt_count = scan_csv_for_corruption()  # Opens file in 'r' mode again

# Operation 4: Write data
write_nutrition_data(data)  # Opens file in 'a' mode
```

**Characteristics:**
- **No persistent file handle:** File opened fresh each time
- **Multiple reads:** Same data may be read multiple times per user action
- **Sequential I/O:** Operations are not concurrent
- **Simple but potentially inefficient:** Good for small files, scales poorly

---

### 7.3 Safe Dictionary Access Pattern 🛡️

**Used throughout file reading:**

```python
# Instead of: row['Name'] (raises KeyError if missing)
# Use:
value = row.get('Name', '')  # Returns empty string if key missing
```

**Why this matters:**
- CSV file could be manually edited
- Column might be missing
- Prevents `KeyError` exceptions
- Allows graceful degradation

---

### 7.4 Try-Continue Pattern for Resilience 🧯

**Used in all read functions:**

```python
for row in reader:
    try:
        # Attempt to process row
        entry_date = datetime.datetime.fromisoformat(row['DateTime'])
        entries.append(row)
    except (ValueError, KeyError):
        continue  # Skip bad row, process rest
```

**Benefits:**
- One corrupted row doesn't crash entire operation
- Valid data is still retrieved
- Error is silently handled (corruption scan reports separately)

---

## 8. Performance Characteristics 🚀

### 8.1 Time Complexity ⏱️

**File Operations:**

| Operation | Opens File | Reads All Rows | Time Complexity |
|-----------|-----------|----------------|------------------|
| `create_csv_file()` | 1 write | No | O(1) |
| `check_csv_file_exists()` | 1 read | No | O(1) |
| `write_nutrition_data()` | 1 append | No | O(1) |
| `get_all_entries()` | 1 read | Yes | O(n) |
| `getEntriesByDate()` | 1 read | Yes | O(n) |
| `getEntriesWithinWeek()` | 1 read | Yes | O(n) |
| `get_entry_by_name()` | 1 read | Partial (breaks on match) | O(n) worst case, O(1) best case |
| `scan_csv_for_corruption()` | 1 read | Yes | O(n) |

Where n = number of rows in CSV

---

### 8.2 I/O Operations Per User Action 🔄

**Example: View entries (Option 3 in main menu)**

```python
entries = data.get_all_entries()  # File opened & read
corrupt_count = data.scan_csv_for_corruption()  # File opened & read again
```

**Total:** 2 file opens, 2 complete reads of all rows

---

### 8.3 Space Complexity 🧠

**In-Memory Storage:**

```python
entries = get_all_entries()  # Loads ALL rows into memory
```

- Entire result set stored in memory as list of dictionaries
- Each dictionary contains 6 key-value pairs
- Space: O(n) where n = number of entries

**For typical usage (hundreds of entries):** Negligible memory impact

**For extreme usage (millions of entries):** Would require refactoring to streaming or pagination

---

### 8.4 Current Limitations ⚠️

1. **Multiple file reads:** Same data read multiple times per operation
    - Viewing entries reads file twice (get_all_entries + scan_csv_for_corruption)
   - Statistics read file, then process in memory

2. **Full table scans:** Every query reads entire file
   - No indexing
   - No optimization for date ranges
   - Every row examined even if only recent data needed

3. **No caching:** Previous reads not stored
   - Could cache in memory after first read
   - Would need invalidation on write

4. **Append-only writes:** No update or delete operations
   - Duplicate entries possible
   - Manual file editing required to remove entries

---

### 8.5 Scalability Considerations 📈

**Current design works well for:**
- ✅ Personal use (single user)
- ✅ Dozens to hundreds of entries
- ✅ Daily interaction patterns
- ✅ Simple queries

**Would need refactoring for:**
- ❌ Thousands of entries (slow full scans)
- ❌ High-frequency writes (file open/close overhead)
- ❌ Concurrent access (no locking mechanism)
- ❌ Complex queries (no query optimization)

---

## Summary 📌

### File Processing Workflow

```
┌─────────────────────────────────────────────────────────┐
│                    Program Start                         │
└────────────────────┬────────────────────────────────────┘
                     │
                     │
         ┌───────────┴───────────┐
         │ check_csv_file_exists()  │
         │  - Try open 'r' mode  │
         │  - If missing: create │
         └───────────┬───────────┘
                     │
         ┌───────────▼───────────────────────────────────┐
         │              Main Loop                         │
         │  - Show menu                                   │
         │  - Get user choice                             │
         └───────────┬───────────────────────────────────┘
                     │
         ┌───────────▼───────────┐
         │    User Action         │
         └───────────┬───────────┘
                     │
      ┌──────────────┼──────────────┐
      │              │              │
      ▼              ▼              ▼
  [WRITE]        [READ]        [QUERY]
      │              │              │
      ▼              ▼              ▼
write_nutrition  get_all_entries  get_entries_by_date
  Data()                        getEntriesWithinWeek
    - Open 'a'     - Open 'r'     get_entry_by_name
  - Append row   - DictReader   
  - Close        - Filter       - Open 'r'
                 - Return list  - DictReader
                 - Close        - Filter by criteria
                                - Return matches
                                - Close
```

---

### Key Takeaways

1. **Simple CSV persistence** using Python's built-in csv module
2. **Defensive reading** with validation and error handling
3. **Append-only writes** for data integrity
4. **Dictionary-based access** via csv.DictReader for clarity
5. **Context managers** ensure proper file cleanup
6. **Multiple file opens** per operation (trade simplicity for performance)
7. **Resilient processing** that skips corrupted data without crashing

---

**Last Updated:** November 27, 2025
