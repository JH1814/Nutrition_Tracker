# ✅ Data Validation Documentation

This document describes all validation mechanisms implemented in the Nutrition Tracker application, including input validation, data integrity checks, and error handling strategies. Architecture-wise the program uses a pragmatic separation of modules: `ui.py` (interaction + validation loops), `main.py` (flow coordination), and `data.py` (persistence + analytics). This document focuses purely on validation behavior independent of any formal pattern naming.

---

## Table of Contents 📚
1. [User Input Validation](#user-input-validation)
2. [CSV Data Validation](#csv-data-validation)
3. [Corruption Detection & Handling](#corruption-detection--handling)
4. [File System Validation](#file-system-validation)
5. [Statistics Calculation Validation](#statistics-calculation-validation)
6. [Exception Handling in Main Application](#exception-handling-in-main-application)
7. [Summary of Validation Layers](#summary-of-validation-layers)

---

## 1. User Input Validation 👤

### 1.1 String Input Validation (`ui.py`) 🔤

**Function:** `getStringInput(message: str) -> str`

**What is validated:**
- Input cannot be empty
- Input cannot be a pure numeric value
- Input must be a valid string
- Input length must be ≤ 30 characters

**How it works:**
```python
def getStringInput(message: str) -> str:  
    is_valid = False
    while not is_valid:
        try: 
            string = input(message)
            if not string or string.isdigit():
                raise ValueError("Input Cannot be Empty or a Number.")
            if len(string) > 30:
                raise ValueError("Input Too Long (max 30 characters).")
            is_valid = True
        except ValueError as e:
            print(f"Invalid Input. Please Enter a Valid String. {e}")
    return string
```

**Validation logic:**
- Loops until valid input is provided
- Checks if input is empty using `not string`
- Checks if input is purely numeric using `string.isdigit()`
- Checks maximum length using `len(string) > 30`
- Raises `ValueError` with descriptive message for invalid input
- Catches exception and prompts user again

**Used for:** Food/recipe names

---

### 1.2 Float Input Validation (`ui.py`) 🔢

**Function:** `getFloatInput(message: str) -> float`

**What is validated:**
- Input must be convertible to a floating-point number
- Handles decimal values

**How it works:**
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

**Validation logic:**
- Attempts to cast input to `float`
- Catches `ValueError` if conversion fails
- Loops until valid numeric input is provided

**Used for:** Protein, Fat, Carbs, and Calories values

---

### 1.3 Integer Input Validation (`ui.py`) 🔢

**Function:** `getIntInput(message: str) -> int`

**What is validated:**
- Input must be convertible to an integer
- No decimal values allowed

**How it works:**
```python
def getIntInput(message: str) -> int:
    is_valid = False
    while not is_valid:
        try: 
            integer = int(input(message))
            is_valid = True
        except ValueError as e:
            print(f"Invalid Input. Please Enter a Valid Integer. {e}")
    return integer
```

**Validation logic:**
- Attempts to cast input to `int`
- Catches `ValueError` if conversion fails
- Loops until valid integer is provided

**Used for:** Menu choices and selection options

---

## 2. CSV Data Validation 🗃️

### 2.1 Name Field Validation

**What is validated:**
- Name field must not be empty
- Name field must not contain only whitespace

**Implementation across functions:**

```python
# In getAllEntries()
if not row.get('Name', '').strip():
    continue  # Skip corrupted row
```

```python
# In getEntriesByDate()
if not row.get('Name', '').strip():
    continue  # Skip corrupted row
```

```python
# In getEntriesWithinWeek()
if not row.get('Name', '').strip():
    continue  # Skip corrupted row
```

```python
# In getEntryByName()
if not row.get('Name', '').strip():
    continue  # Skip corrupted row
```

**Validation logic:**
- Uses `row.get('Name', '')` to safely retrieve value with empty string default
- Applies `.strip()` to remove leading/trailing whitespace
- Uses boolean evaluation: empty string after strip evaluates to `False`
- Skips row using `continue` if validation fails

**Purpose:** Prevents processing of corrupted CSV rows with missing or blank names

---

### 2.2 DateTime Field Validation

**What is validated:**
- DateTime field must exist
- DateTime must be in valid ISO 8601 format
- DateTime must be parseable by Python's `datetime.fromisoformat()`

**Implementation in data retrieval functions:**

```python
# In getEntriesByDate()
try:
    if not row.get('Name', '').strip():
        continue
    entry_date = datetime.datetime.fromisoformat(row['DateTime']).date()
    if entry_date == date:
        entries.append(row)
except (ValueError, KeyError):
    continue  # Skip entries with invalid datetime or missing fields
```

```python
# In getEntriesWithinWeek()
try:
    if not row.get('Name', '').strip():
        continue
    entry_date = datetime.datetime.fromisoformat(row['DateTime'])
    if entry_date >= one_week_ago:
        entries.append(row)
except (ValueError, KeyError):
    continue  # Skip entries with invalid datetime or missing fields
```

**Validation logic:**
- Wraps datetime parsing in try-except block
- Uses `datetime.fromisoformat()` which validates ISO format
- Catches `ValueError` for malformed datetime strings
- Catches `KeyError` if 'DateTime' field is missing entirely
- Silently skips invalid rows to keep program running

**Valid DateTime formats:**
- `"2025-11-27T14:30:00"`
- `"2025-11-27"`
- Any ISO 8601 compliant format

---

## 3. Corruption Detection & Handling ⚠️

### 3.1 Corruption Scanning Function

**Function:** `scanCsvForCorruption() -> int`

**What is validated:**
- Entire CSV file is scanned for corrupted rows
- Returns count of corrupted entries

**Implementation:**
```python
def scanCsvForCorruption() -> int:
    """Scan the CSV for corrupted rows and return the count.

    A row is considered corrupted if:
    - The 'Name' field is empty or missing
    - The 'DateTime' field is missing or not a valid ISO datetime

    This function does not modify data; it only reports issues.
    """
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

**Corruption criteria:**
1. **Empty Name:** `not row.get('Name', '').strip()`
2. **Invalid DateTime:** Exception raised by `datetime.fromisoformat()`

**Key features:**
- Non-destructive scan (reads only, doesn't modify)
- Uses underscore `_` for unused DateTime variable (throwaway pattern)
- Catches broad `Exception` to handle any datetime parsing errors
- Returns total count for reporting

**Usage in application:**
```python
# In main.py - After viewing entries
corrupt_count = data.scanCsvForCorruption()
if corrupt_count > 0:
    ui.showEntriesFailed(f"Warning: {corrupt_count} corrupted row(s) were skipped.")
```

---

### 3.2 Resilient Data Retrieval

**Strategy:** All data retrieval functions skip corrupted rows instead of crashing

**Example from `getAllEntries()`:**
```python
def getAllEntries() -> list:
    entries = []
    with open(csv_file_path,'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Skip rows with empty name field (corrupted data)
            if not row.get('Name', '').strip():
                continue  # SKIP instead of RAISE
            entries.append(row)
    return entries
```

**Design principle:**
- **Before:** Program crashed on corrupted data (raised exceptions)
- **After:** Program continues, skips bad data, warns user
- Valid entries are still returned and displayed
- Corruption warning shown separately after successful operations

---

## 4. File System Validation 🗂️

### 4.1 CSV File Existence Check

**Function:** `checkCsvFileExists() -> None`

**What is validated:**
- CSV file exists at expected path (`./data/data.csv`)
- File is readable

**Implementation:**
```python
def checkCsvFileExists() -> None:
    exists = False
    while not exists:
        try:
            with open(csv_file_path, "r") as file:
                exists = True
        except FileNotFoundError:
            createCsvFile()
```

**Validation logic:**
- Attempts to open file in read mode
- If successful, sets `exists = True` and exits loop
- If `FileNotFoundError` is raised, creates new file with headers
- Guarantees file exists before any read/write operations

**Auto-recovery:** Automatically creates file with proper headers if missing

---

### 4.2 CSV File Creation

**Function:** `createCsvFile() -> None`

**What is created:**
- New CSV file with proper column headers

**Implementation:**
```python
def createCsvFile() -> None:
    with open(csv_file_path, "w") as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Protein", "Fat", "Carbs", "Calories", "DateTime"])
```

**Ensures:**
- Consistent column structure
- Proper headers for `csv.DictReader` to map keys
- File is created in write mode (overwrites if exists)

---

## 5. Statistics Calculation Validation 📊

### 5.1 Daily Totals Calculation

**Function:** `getDailyTotals() -> list[dict]`

**What is validated:**
- Entries exist for the requested date
- Numeric fields are convertible to float
- Malformed numeric values are skipped

**Implementation:**
```python
def getDailyTotals() -> list[dict]:
    entries = getEntriesByDate()

    if not entries:
        return None  # Explicit null return for empty data

    total_protein = 0.0
    total_fat = 0.0
    total_carbs = 0.0
    total_calories = 0.0

    for entry in entries:
        try:
            total_protein += float(entry.get('Protein', 0))
            total_fat += float(entry.get('Fat', 0))
            total_carbs += float(entry.get('Carbs', 0))
            total_calories += float(entry.get('Calories', 0))
        except ValueError:
            pass  # Skip malformed entries

    return [{
        'Protein': round(total_protein, 2), 
        'Fat': round(total_fat, 2), 
        'Carbs': round(total_carbs, 2), 
        'Calories': round(total_calories, 2)
    }]
```

**Validation logic:**
1. **Empty check:** Returns `None` if no entries found
2. **Safe field access:** Uses `.get(field, 0)` with default value
3. **Type conversion:** Wraps `float()` conversion in try-except
4. **Error handling:** Silently skips entries with malformed numeric values
5. **Precision:** Rounds results to 2 decimal places

**Resilience:** Bad numeric data doesn't crash calculation, just skipped

---

### 5.2 Weekly Averages Calculation

**Function:** `getWeeklyAverages() -> list[dict]`

**What is validated:**
- Same validations as daily totals
- Additionally calculates averages (divides by count)

**Implementation:**
```python
def getWeeklyAverages() -> list[dict]:
    entries = getEntriesWithinWeek()

    if not entries:
        return None  # Explicit null return

    total_protein = 0.0
    total_fat = 0.0
    total_carbs = 0.0
    total_calories = 0.0

    for entry in entries:
        try:
            total_protein += float(entry.get('Protein', 0))
            total_fat += float(entry.get('Fat', 0))
            total_carbs += float(entry.get('Carbs', 0))
            total_calories += float(entry.get('Calories', 0))
        except ValueError:
            pass  # Skip malformed entries
    
    count = len(entries)
    return [{
        'Protein': round(total_protein / count, 2),
        'Fat': round(total_fat / count, 2),
        'Carbs': round(total_carbs / count, 2),
        'Calories': round(total_calories / count, 2)
    }]
```

**Additional validation:**
- Division by `count` (len of entries)
- Safe because `if not entries` check prevents division by zero

---

## 6. Exception Handling in Main Application 🧯

### 6.1 Add Nutrition Entry (Choice 1)

**Exceptions handled:**
```python
try:
    data.checkCsvFileExists()
    data.writeNutritionData([name, protein, fat, carbs, calories, datetime.datetime.now()])
    ui.addNutritionSuccessfull()
except FileNotFoundError as e:
    data.createCsvFile()
    ui.addNutritionFailed(e)
```

**Validation:**
- Catches `FileNotFoundError` if file deleted during operation
- Automatically recreates file
- Displays failure message to user

---

### 6.2 Use Existing Entry (Choice 2)

**Exceptions handled:**
```python
try:
    entry = data.getEntryByName(recipe)
except FileNotFoundError as e:
    data.createCsvFile()
    ui.addNutritionFailed(e)
except ValueError as e:
    ui.addNutritionFailed(e)

if entry:
    try:
        data.writeNutritionData((entry[0]["Name"], ...))
        ui.addNutritionSuccessfull()
    except FileNotFoundError as e:
        data.createCsvFile()
        ui.addNutritionFailed(e)
else:
    ui.addNutritionFailed("Recipe Not Found in the Nutrition Entries List.")
```

**Validation:**
- Catches `FileNotFoundError` and `ValueError`
- Checks if entry exists before attempting to write
- Provides specific error message if recipe not found

---

### 6.3 View Entries (Choice 3)

**Exceptions handled:**
```python
try:
    entries = data.getAllEntries()
    ui.showEntries(entries, "Nutrition Entries:")
    # Corruption detection
    try:
        corrupt_count = data.scanCsvForCorruption()
        if corrupt_count > 0:
            ui.showEntriesFailed(f"Warning: {corrupt_count} corrupted row(s) were skipped.")
    except IOError:
        pass  # Skip warning if scan fails
except FileNotFoundError as e:
    data.createCsvFile()
    ui.showEntriesFailed(e)
except IndexError as e:
    ui.showEntriesFailed(e)
```

**Validation:**
- Nested try-except for corruption scanning (non-blocking)
- Handles missing file, empty data, and index errors
- Shows valid data even if corruption scan fails

---

### 6.4 Statistics (Choice 4)

**Exceptions handled:**
```python
try:
    if stats_choice == 1:
        totals = data.getDailyTotals()
        if totals:
            ui.showEntries(totals, "Daily Total Intake")
            # Corruption warning
        else:
            ui.showEntriesFailed("No Entries Found for Today")
            # Corruption warning
    # Similar for weekly averages...
except FileNotFoundError as e:
    data.createCsvFile()
    ui.showEntriesFailed(e)
except IOError as e:
    ui.showEntriesFailed(e)
except ValueError as e:
    ui.showEntriesFailed(e)
```

**Validation:**
- Checks for `None` return (no data available)
- Handles file, IO, and value errors
- Attempts corruption detection even when no entries found

---

## 7. Summary of Validation Layers 🧱

### Layer 1: Input Validation (UI)
- String, float, and integer type checking
- Empty input prevention
- Loop-until-valid pattern

### Layer 2: Data Structure Validation (CSV Reading)
- Name field presence and content
- DateTime field format and parseability
- Safe dictionary access with defaults

### Layer 3: Corruption Detection (Scanning)
- Dedicated scan function for reporting
- Non-blocking corruption checks
- User warnings without crashing

### Layer 4: File System Validation
- File existence checks
- Automatic file creation with headers
- Exception handling for IO errors

### Layer 5: Calculation Validation (Statistics)
- Empty data checks (return None)
- Numeric conversion error handling
- Division by zero prevention

### Layer 6: Application-Level Exception Handling
- Try-except blocks in main flow
- User-friendly error messages
- Auto-recovery where possible

---

## Design Philosophy 💡

The validation system follows these core principles:

1. **Fail gracefully:** Never crash, always inform user
2. **Skip bad data:** Invalid rows don't prevent processing valid ones
3. **Auto-recovery:** Create missing files, handle missing fields
4. **User awareness:** Report corruption but don't block operations
5. **Defense in depth:** Multiple validation layers protect data integrity
6. **Explicit over implicit:** Clear validation checks with descriptive error messages

---

## Common Validation Patterns 🧩

### Pattern 1: Safe Dictionary Access
```python
value = row.get('FieldName', default_value)
```
Never raises `KeyError`, returns default if missing

### Pattern 2: Whitespace-Aware String Validation
```python
if not string_value.strip():
    # Handle empty or whitespace-only string
```

### Pattern 3: Try-Continue for Resilience
```python
for row in data:
    try:
        # Process row
    except SomeException:
        continue  # Skip bad row, process rest
```

### Pattern 4: Early Return on Invalid State
```python
if not entries:
    return None  # Signal no data available
```

### Pattern 5: Nested Exception Handling
```python
try:
    # Critical operation
    try:
        # Optional enhancement (like warnings)
    except Exception:
        pass  # Don't let optional feature break main flow
except Exception:
    # Handle critical failure
```
