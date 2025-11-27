# Nutrition Tracker - User Manual

**Version 1.0** | **Last Updated:** November 27, 2025

Welcome to the Nutrition Tracker! This manual will guide you through all features and show you how to effectively track your daily nutrition intake. Internally the program is organized by purpose (flow coordinator in `main.py`, interaction in `ui.py`, data/analytics in `data.py`) rather than a formal named architecture pattern—this keeps usage simple and predictable.

---

## Table of Contents

1. [Getting Started](#getting-started)
2. [Main Menu Overview](#main-menu-overview)
3. [Adding Nutrition Entries](#adding-nutrition-entries)
4. [Reusing Existing Entries](#reusing-existing-entries)
5. [Viewing Your Entries](#viewing-your-entries)
6. [Statistics & Analytics](#statistics--analytics)
7. [Tips & Best Practices](#tips--best-practices)
8. [Troubleshooting](#troubleshooting)
9. [Data Management](#data-management)

---

## 1. Getting Started

### System Requirements
- Python 3.x installed
- Terminal/Command Prompt access
- ~10 MB of free disk space

### Starting the Application

**On Windows:**
```bash
cd path\to\Nutrition_Tracker\src
python main.py
```

**On Mac/Linux:**
```bash
cd path/to/Nutrition_Tracker/src
python3 main.py
```

### First Launch

When you start the program for the first time, it will automatically:
1. Create a `data` folder
2. Create a `data.csv` file with proper headers
3. Display the main menu

```
┌─────────────────────────────────────────────┐
│  Welcome to the Nutrition Tracker!          │
│  1. Add Nutrition Entry                     │
│  2. Use Existing Nutrition Entry            │
│  3. View Nutrition Entries                  │
│  4. View Statistics                         │
│  5. Exit                                    │
└─────────────────────────────────────────────┘
```

---

## 2. Main Menu Overview

### Navigation

The program uses **number-based navigation**:
- Type the number of your choice
- Press **Enter** to confirm
- Invalid choices will show an error and return to the menu

### Menu Structure

```
Main Menu
├── 1. Add Nutrition Entry ─────────────► Add new food item
├── 2. Use Existing Entry ──────────────► Reuse saved recipe
├── 3. View Nutrition Entries ──────────► See all logged items
├── 4. View Statistics ─────────────────┐
│   └── Submenu:                        │
│       ├── 1. Daily Totals ────────────► Today's sum
│       ├── 2. Weekly Averages ─────────► 7-day average
│       └── 3. Back to Main Menu        │
└── 5. Exit ────────────────────────────► Close program
```

---

## 3. Adding Nutrition Entries

### Purpose
Log a new food item with its nutritional information.

### Step-by-Step Process

```
┌─────────────────────────────────────────────┐
│            STEP 1: Select Option            │
│  Enter your Choice: 1                       │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│            STEP 2: Enter Food Name          │
│  Add Name of Nutrition Entry: Chicken Salad │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│        STEP 3: Enter Protein (grams)        │
│  Add Protein in grams: 35                   │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│          STEP 4: Enter Fat (grams)          │
│  Add Fat in grams: 12                       │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│         STEP 5: Enter Carbs (grams)         │
│  Add Carbs in grams: 25                     │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│       STEP 6: Enter Calories (kcal)         │
│  Add Calories in kcal: 350                  │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│         ✓ SUCCESS MESSAGE                   │
│  Nutrition Data Added Successfully!         │
└─────────────────────────────────────────────┘
```

### Input Requirements

| Field | Type | Rules | Example |
|-------|------|-------|---------|
| **Name** | Text | • Cannot be empty<br>• Cannot be only numbers<br>• Max 30 characters<br>• Use descriptive names | `"Chicken Salad"` |
| **Protein** | Number | • Must be numeric<br>• Can have decimals<br>• Use grams | `35` or `35.5` |
| **Fat** | Number | • Must be numeric<br>• Can have decimals<br>• Use grams | `12` or `12.3` |
| **Carbs** | Number | • Must be numeric<br>• Can have decimals<br>• Use grams | `25` or `25.8` |
| **Calories** | Number | • Must be numeric<br>• Can have decimals<br>• Use kilocalories | `350` or `350.5` |

### What Happens Behind the Scenes

```
User Input → Validation → Storage → Confirmation
    │            │           │           │
    │            │           │           └─► Success message
    │            │           │
    │            │           └─► Entry saved to CSV with timestamp
    │            │
    │            └─► Input checked for errors
    │
    └─► Values collected
```

### Example Session

```
Add Name of Nutrition Entry: Greek Yogurt with Berries
Add Protein in grams: 15
Add Fat in grams: 5
Add Carbs in grams: 30
Add Calories in kcal: 220

✓ Nutrition Data Added Successfully!

[Automatically returns to main menu]
```

### Automatic Timestamp

The program automatically records:
- **Date:** When the entry was added
- **Time:** Exact hour, minute, second
- **Format:** `2025-11-27 14:30:15.123456`

You don't need to enter this manually!

---

## 4. Reusing Existing Entries

### Purpose
Quickly log a meal you've eaten before without re-entering all the nutrition data.

### When to Use This Feature

✅ **Perfect for:**
- Daily breakfast items (e.g., "Oatmeal")
- Regular snacks (e.g., "Protein Shake")
- Favorite meals (e.g., "Chicken and Rice")
- Meal prep items

❌ **Not suitable for:**
- New foods not yet in your database
- Modified recipes with different portions

### Process Visualization

```
┌────────────────────────────────────────┐
│  Select Option 2                       │
└───────────────┬────────────────────────┘
                │
                ▼
┌────────────────────────────────────────┐
│  Enter the recipe name                 │
│  "Pizza"                               │
└───────────────┬────────────────────────┘
                │
                ▼
        ┌───────────────┐
        │  Search CSV   │
        │  for "Pizza"  │
        └───────┬───────┘
                │
        ┌───────▼────────┐
        │  Found?        │
        └───┬────────┬───┘
            │        │
           YES       NO
            │        │
            │        └──► "Recipe Not Found"
            │                    │
            ▼                    ▼
    ┌────────────┐         Return to Menu
    │ Copy Values│
    │ New Time   │
    └─────┬──────┘
          │
          ▼
    ┌────────────┐
    │  Save to   │
    │   CSV      │
    └─────┬──────┘
          │
          ▼
    "Success!"
```

### Step-by-Step Example

**Scenario:** You had pizza yesterday and want to log it again today.

```bash
# STEP 1: Select option
Enter your Choice: 2

# STEP 2: Enter exact name (case-sensitive)
Enter the Name of the Recipe to use: Pizza

# STEP 3: Program searches and adds entry
✓ Nutrition Data Added Successfully!
```

### Important Notes

⚠️ **Name must match exactly:**
- `"Pizza"` ≠ `"pizza"` ≠ `"Pizza "` (with space)
- Use the exact same spelling and capitalization
- Check your entries (Option 3) if you're unsure of the exact name

🕐 **New timestamp applied:**
- Original entry: `2025-11-26 12:00:00`
- New entry: `2025-11-27 14:30:00` (current time)

💾 **Creates new row:**
- Does NOT modify original entry
- Adds a duplicate with current timestamp
- Both entries remain in your history

### Comparison: Add vs. Reuse

| Aspect | Add New (Option 1) | Reuse Existing (Option 2) |
|--------|-------------------|---------------------------|
| **Input required** | All 5 fields | Only name |
| **Time taken** | ~30 seconds | ~5 seconds |
| **Use case** | New foods | Recurring meals |
| **Data accuracy** | Depends on manual entry | Consistent with original |

---

## 5. Viewing Your Entries

### Purpose
See all nutrition entries you've logged, with automatic data quality checks.

### Display Format

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                          Nutrition Entries:                                   │
├──────────────────────────────────────────────────────────────────────────────┤
│ Name                           Protein    Fat        Carbs      Calories     │
├──────────────────────────────────────────────────────────────────────────────┤
│ Chicken Salad                  35g        12g        25g        350 kcal     │
│ Pizza                          30g        7.5g       200g       600 kcal     │
│ Greek Yogurt                   15g        5g         30g        220 kcal     │
│ Oatmeal with Berries          6g         4g         45g        240 kcal     │
│ Protein Shake                  30g        2g         8g         180 kcal     │
└──────────────────────────────────────────────────────────────────────────────┘

Press Enter to continue...
```

### Table Columns Explained

| Column | Description | Example |
|--------|-------------|---------|
| **Name** | Food item description | `Chicken Salad` |
| **Protein** | Protein content in grams | `35g` |
| **Fat** | Fat content in grams | `12g` |
| **Carbs** | Carbohydrate content in grams | `25g` |
| **Calories** | Energy content in kilocalories | `350 kcal` |

**Note:** The DateTime field is stored but not displayed in the list view.

### Data Quality Warnings

If corrupted data is detected, you'll see:

```
┌──────────────────────────────────────────────────────────────────┐
│  ⚠ Warning: 2 corrupted row(s) were skipped.                     │
└──────────────────────────────────────────────────────────────────┘
```

**What causes corruption?**
- Empty food names
- Invalid timestamps
- Missing required fields

**What happens?**
- ✓ Valid entries are still displayed
- ✗ Corrupted entries are skipped (not shown)
- ℹ You receive a count of skipped rows

### Empty List

If you haven't added any entries yet:

```
┌──────────────────────────────────────────────────────────────────┐
│  No Entries Found: No Entries Found.                             │
└──────────────────────────────────────────────────────────────────┘
```

---

## 6. Statistics & Analytics

### Accessing Statistics

```
Main Menu → Option 4 → Statistics Menu
```

### Statistics Submenu

```
┌─────────────────────────────────────────────┐
│         Statistics Menu:                    │
│  1. Daily Totals                            │
│  2. Weekly Averages                         │
│  3. Back to Main Menu                       │
└─────────────────────────────────────────────┘
```

---

### 6.1 Daily Totals (Option 1)

**Purpose:** See the sum of all nutrition consumed today.

#### What It Shows

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                         Daily Total Intake                                    │
├──────────────────────────────────────────────────────────────────────────────┤
│ Name                           Protein    Fat        Carbs      Calories     │
├──────────────────────────────────────────────────────────────────────────────┤
│                                116g       48.5g      328g       1940 kcal    │
└──────────────────────────────────────────────────────────────────────────────┘

Press Enter to continue...
```

#### Calculation Method

```
Today's Entries (example):
┌──────────────────────┬─────────┬──────┬────────┬──────────┐
│ Breakfast: Oatmeal   │ 6g      │ 4g   │ 45g    │ 240 kcal │
│ Lunch: Chicken Salad │ 35g     │ 12g  │ 25g    │ 350 kcal │
│ Snack: Protein Shake │ 30g     │ 2g   │ 8g     │ 180 kcal │
│ Dinner: Salmon       │ 45g     │ 30.5g│ 250g   │ 1170 kcal│
└──────────────────────┴─────────┴──────┴────────┴──────────┘
                         ↓ SUM ↓
                    ┌──────────────────────────┐
                    │ Total: 116g, 48.5g,      │
                    │        328g, 1940 kcal   │
                    └──────────────────────────┘
```

#### Use Cases

✓ **Track daily goals:**
- "Have I hit my protein target today?"
- "Am I staying within my calorie limit?"

✓ **Plan remaining meals:**
- "I need 20g more protein today"
- "I have 400 calories left for dinner"

#### No Data Message

If you haven't logged anything today:

```
┌──────────────────────────────────────────────────────────────────┐
│  No Entries Found: No Entries Found for Today                    │
└──────────────────────────────────────────────────────────────────┘
```

---

### 6.2 Weekly Averages (Option 2)

**Purpose:** Understand your average daily intake over the past 7 days.

#### What It Shows

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                        Weekly Average Intake                                  │
├──────────────────────────────────────────────────────────────────────────────┤
│ Name                           Protein    Fat        Carbs      Calories     │
├──────────────────────────────────────────────────────────────────────────────┤
│                                93.5g      38.2g      267.8g     1583.3 kcal  │
└──────────────────────────────────────────────────────────────────────────────┘

Press Enter to continue...
```

#### Calculation Method

```
Last 7 Days (example):
┌──────────────┬──────────────────────────────────────┐
│ Nov 21       │ 3 entries → 85g protein, 1450 cal   │
│ Nov 22       │ 4 entries → 102g protein, 1620 cal  │
│ Nov 23       │ 3 entries → 88g protein, 1510 cal   │
│ Nov 24       │ 5 entries → 96g protein, 1680 cal   │
│ Nov 25       │ 2 entries → 90g protein, 1530 cal   │
│ Nov 26       │ 4 entries → 101g protein, 1650 cal  │
│ Nov 27       │ 4 entries → 93g protein, 1560 cal   │
└──────────────┴──────────────────────────────────────┘
                      ↓ AVERAGE ↓
            ┌────────────────────────────┐
            │ Avg per Entry: 93.5g,      │
            │                1583.3 kcal │
            └────────────────────────────┘
```

**Note:** Average is calculated **per entry**, not per day!

#### Use Cases

✓ **Identify trends:**
- "My average protein is lower than I thought"
- "I'm averaging 200 more calories than my goal"

✓ **Compare weeks:**
- Run weekly averages every Sunday
- Compare this week to last week

✓ **Adjust habits:**
- "I need to add more protein sources"
- "My carb intake is consistent"

#### Time Window

The calculation includes entries from:
- **Start:** 7 days ago from current moment
- **End:** Right now

**Example:**
- Current time: `Nov 27, 2025 14:30`
- Window: `Nov 20, 2025 14:30` to `Nov 27, 2025 14:30`

---

### 6.3 Statistics Tips

#### Best Practices

📊 **Check daily totals:**
- At the end of each day
- Before planning your last meal

📈 **Review weekly averages:**
- Every Sunday evening
- Track progress over time

📝 **Keep notes separately:**
- The program doesn't store goals
- Use a notebook or spreadsheet for target values
- Compare your results to your goals manually

---

## 7. Tips & Best Practices

### Data Entry Tips

#### ✓ DO:

**Use consistent naming:**
```
✓ "Chicken Salad"
✓ "Chicken Salad with Ranch"
✗ "chicken salad" (lowercase)
✗ "Chkn Salad" (abbreviation)
```

**Be specific:**
```
✓ "Pizza - Pepperoni (2 slices)"
✓ "Protein Shake - Chocolate"
✗ "Pizza" (which kind? how much?)
```

**Round numbers reasonably:**
```
✓ 35g (simple)
✓ 35.5g (one decimal okay)
✗ 35.4762g (too precise)
```

**Log immediately:**
- Enter data right after eating
- Don't wait until end of day (you'll forget!)

#### ✗ DON'T:

**Don't use special characters excessively:**
```
✗ "Chicken!!!!" 
✗ "Pizza $$$"
```

**Don't duplicate intentionally:**
```
✗ Creating multiple entries with same name but different values
   (Makes "Use Existing Entry" confusing)
```

**Don't estimate wildly:**
- Use nutrition labels when available
- Look up values online if needed
- Consistency matters more than perfection

---

### Workflow Examples

#### Morning Routine

```
1. Eat breakfast
2. Open Nutrition Tracker
3. Option 1 → Add Entry
4. Enter breakfast details
5. Option 5 → Exit

Total time: 2-3 minutes
```

#### Evening Review

```
1. Open Nutrition Tracker
2. Option 4 → Statistics
3. Option 1 → See today's totals
4. Compare to your goals
5. Option 3 → Back to main menu
6. Option 5 → Exit

Total time: 1 minute
```

#### Weekly Check-in

```
Sunday evening:
1. Option 4 → Statistics
2. Option 2 → Weekly Averages
3. Write down the averages
4. Compare to last week's averages
5. Adjust meal plans if needed

Total time: 2-3 minutes
```

---

## 8. Troubleshooting

### Common Issues

#### Issue: "Invalid Input" Error

**Symptoms:**
```
Add Protein in grams: abc
Invalid Input. Please Enter a Valid Number.
```

**Solution:**
- Only enter numbers (digits)
- Use decimal point (`.`) not comma (`,`)
- Don't include units (type `35`, not `35g`)

---

#### Issue: "Recipe Not Found"

**Symptoms:**
```
Failed to Add Nutrition Data: Recipe Not Found in the Nutrition Entries List.
```

**Solution:**
1. Check spelling (case-sensitive)
2. View entries (Option 3) to see exact names
3. Look for extra spaces
4. If truly missing, use Option 1 to add it first

---

#### Issue: Corrupted Data Warning

**Symptoms:**
```
⚠ Warning: 3 corrupted row(s) were skipped.
```

**Causes:**
- Manually edited CSV file incorrectly
- Program crashed during write operation
- Missing data in CSV rows

**Solutions:**

**Option A: Ignore**
- Valid data still works fine
- Corrupted rows are simply skipped

**Option B: Manual cleanup**
1. Navigate to `./data/data.csv`
2. Open in text editor
3. Look for rows with:
   - Empty name field
   - Missing commas
   - Invalid date formats
4. Delete corrupted rows
5. Save file

**Option C: Start fresh**
1. Close program
2. Delete `./data/data.csv`
3. Restart program (creates new file)
4. Re-enter data

---

#### Issue: Program Won't Start

**Symptoms:**
```
python main.py
ModuleNotFoundError: No module named 'data'
```

**Solution:**
Make sure you're in the correct directory:
```bash
# Navigate to src folder
cd path/to/Nutrition_Tracker/src

# Then run
python main.py
```

---

#### Issue: File Permission Error

**Symptoms:**
```
PermissionError: [Errno 13] Permission denied: './data/data.csv'
```

**Solution:**
1. Close any programs that have the CSV file open (Excel, text editors)
2. Check file permissions (should be readable/writable)
3. On Linux/Mac: `chmod 644 ./data/data.csv`

---

### Getting Help

If you encounter an issue not listed here:

1. **Check the error message** - Often contains helpful information
2. **Try restarting** - Close and reopen the program
3. **Check file integrity** - Look at `./data/data.csv` in a text editor
4. **Backup data** - Copy `data.csv` to a safe location
5. **Reinstall** - Delete and re-download the program files

---

## 9. Data Management

### Where Your Data is Stored

```
Nutrition_Tracker/
└── src/
    └── data/
        └── data.csv  ← Your nutrition data is here
```

**Full path examples:**
- Windows: `C:\Users\YourName\Nutrition_Tracker\src\data\data.csv`
- Mac: `/Users/YourName/Nutrition_Tracker/src/data/data.csv`
- Linux: `/home/yourname/Nutrition_Tracker/src/data/data.csv`

---

### Backing Up Your Data

#### Manual Backup (Recommended weekly)

1. Navigate to the `data` folder
2. Copy `data.csv`
3. Paste to a backup location
4. Rename with date: `data_backup_2025-11-27.csv`

```
Backup Strategy:
└── My Documents/
    └── Nutrition_Backups/
        ├── data_backup_2025-11-20.csv
        ├── data_backup_2025-11-27.csv
        └── data_backup_2025-12-04.csv
```

#### Automated Backup (Advanced)

**Windows (Task Scheduler):**
```batch
copy "C:\Path\To\data.csv" "C:\Path\To\Backups\data_%date%.csv"
```

**Mac/Linux (cron job):**
```bash
cp ~/Nutrition_Tracker/src/data/data.csv ~/Backups/data_$(date +%Y%m%d).csv
```

---

### Exporting Data

#### For Excel Analysis

1. Locate `data.csv`
2. Right-click → Open with → Microsoft Excel
3. Data will load as a table
4. Create charts, pivot tables, etc.

#### For Google Sheets

1. Open Google Sheets
2. File → Import
3. Upload tab → Choose `data.csv`
4. Import data

---

### Data Format Reference

**CSV Structure:**
```csv
Name,Protein,Fat,Carbs,Calories,DateTime
Chicken Salad,35,12,25,350,2025-11-27 14:30:15.123456
Pizza,30,7.5,200,600,2025-11-27 18:45:30.987654
```

**Field Definitions:**
- **Name:** String (text)
- **Protein:** Float (decimal number)
- **Fat:** Float (decimal number)
- **Carbs:** Float (decimal number)
- **Calories:** Float (decimal number)
- **DateTime:** ISO 8601 format (`YYYY-MM-DD HH:MM:SS.microseconds`)

---

### Cleaning Up Old Data

If your CSV file gets very large (thousands of entries):

#### Option 1: Archive Old Data
```
1. Create new file: data_archive_2024.csv
2. Copy old entries to archive
3. Delete old entries from data.csv
4. Keep only recent months in active file
```

---

## 10. Quick Reference Card

### Menu Navigation
```
┌─────────────────────────────────────────────────────────────┐
│  Main Menu                                                   │
│  ├─ 1: Add Entry ──────► Enter 5 values ──► Save          │
│  ├─ 2: Use Existing ───► Enter name ──────► Save          │
│  ├─ 3: View Entries ───► See table ───────► Press Enter    │
│  ├─ 4: Statistics ─────► Submenu ─────────► Choose type    │
│  │   ├─ 1: Daily ──────► Today's totals                     │
│  │   ├─ 2: Weekly ─────► 7-day averages                    │
│  │   └─ 3: Back                                             │
│  └─ 5: Exit ───────────► Goodbye message ─► Program ends   │
└─────────────────────────────────────────────────────────────┘
```

### Input Types

| Prompt | Type | Example | Invalid |
|--------|------|---------|---------|
| Name | Text | `Chicken Salad` | `123`, (empty) |
| Protein/Fat/Carbs | Number | `35` or `35.5` | `abc`, `35g` |
| Calories | Number | `350` or `350.2` | `many`, `350kcal` |
| Choice | Integer | `1`, `2`, `3` | `1.5`, `one` |

### File Locations
```
Config:     src/data.py (line 5: csv_file_path)
Data File:  ./data/data.csv
Program:    src/main.py
```

---

## Support & Feedback

### Questions?

If you have questions about using this program:
1. Re-read the relevant section of this manual
2. Check the troubleshooting section
3. Review the CSV file directly to understand data structure

### Found a Bug?

If you discover a problem with the program:
1. Note the exact error message
2. Write down the steps that caused it
3. Check if data was corrupted
4. Report to the development team

---

**Thank you for using Nutrition Tracker!**

Track consistently, analyze regularly, and achieve your nutrition goals. 🥗💪
