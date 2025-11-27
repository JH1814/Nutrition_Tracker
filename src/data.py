"""Data persistence and analytics module for Nutrition Tracker.

This module handles all CSV file operations, data validation, retrieval,
and statistical calculations for nutrition entries.
"""
import csv
import datetime
import os

# variable for CSV path
csv_file_path: str = os.path.join(os.path.dirname(__file__), "data", "data.csv")

def write_nutrition_data(data: list[str | float | datetime.datetime]) -> None:
    """Append a nutrition entry to the CSV file.
    
    Args:
        data: List containing [name, protein, fat, carbs, calories, datetime]
        
    Raises:
        FileNotFoundError: If CSV file doesn't exist (caller should create it)
    """
    with open(csv_file_path, "a", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(data)

#request data functions
def get_all_entries() -> list[dict[str, str]]:
    """Retrieve all valid nutrition entries from the CSV file.
    
    Automatically skips rows with empty Name fields (corrupted data).
    Use scan_csv_for_corruption() to detect and report issues.
    
    Returns:
        List of dictionaries containing valid nutrition entries
        
    Raises:
        FileNotFoundError: If CSV file doesn't exist
    """
    entries = []
    # Track whether any corrupted rows are found
    # Corruption criteria: empty Name or invalid/missing DateTime
    # This function only returns valid entries; use scanCsvForCorruption() to report issues
    with open(csv_file_path, 'r', newline='') as file:
        # Use DictReader to treat each row as a dictionary with column headers as keys
        reader = csv.DictReader(file)
        for row in reader:
            # Skip rows with empty name field (corrupted data)
            if not row.get('Name', '').strip():
                continue
            # Append only valid rows; do not raise to keep program running
            entries.append(row)

    return entries

def scan_csv_for_corruption() -> int:
    """Scan the CSV for corrupted rows and return the count.

    A row is considered corrupted if:
    - The 'Name' field is empty or missing
    - The 'DateTime' field is missing or not a valid ISO datetime

    This function does not modify data; it only reports issues.
    """
    corrupt_count = 0
    with open(csv_file_path, 'r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Check for empty/missing name
            if not row.get('Name', '').strip():
                corrupt_count += 1
                continue
            # Check for invalid DateTime
            try:
                dt_str = row.get('DateTime', '')
                # '_' is a throwaway variable: we only validate parseability
                _ = datetime.datetime.fromisoformat(dt_str)
            except (ValueError, TypeError, KeyError):
                corrupt_count += 1
                continue
    return corrupt_count

def get_entries_by_date(date: datetime.date = datetime.datetime.now().date()) -> list[dict[str, str]]: #get the entries of today
    """Retrieve nutrition entries for a specific date.
    
    Args:
        date: Target date (defaults to today)
        
    Returns:
        List of entries matching the specified date
        
    Note:
        Skips entries with invalid datetime or empty Name fields
    """
    entries = []

    with open(csv_file_path, 'r', newline='') as file:
        # Use DictReader to treat each row as a dictionary with column headers as keys
        reader = csv.DictReader(file)
        for row in reader:
            try:
                # Skip rows with empty name or invalid data
                if not row.get('Name', '').strip():
                    continue
                # Check if the entry is within the last 7 days
                entry_date = datetime.datetime.fromisoformat(row['DateTime']).date()
                if entry_date == date:
                    entries.append(row)
            except (ValueError, KeyError):
                # Skip entries with invalid datetime format or missing fields
                continue

    return entries

def get_entries_within_week() -> list[dict]: #get the entries within last 7 days
    entries = []
    one_week_ago = datetime.datetime.now() - datetime.timedelta(days=7)

    with open(csv_file_path, 'r', newline='') as file:
        # Use DictReader to treat each row as a dictionary with column headers as keys
        reader = csv.DictReader(file)
        for row in reader:
            try:
                # Skip rows with empty name or invalid data
                if not row.get('Name', '').strip():
                    continue
                # Check if the entry is within the last 7 days
                entry_date = datetime.datetime.fromisoformat(row['DateTime'])
                if entry_date >= one_week_ago:
                    entries.append(row)
            except (ValueError, KeyError):
                # Skip entries with invalid datetime format or missing fields
                continue

    return entries

def get_entry_by_name(name: str) -> list[dict[str, str]]:
    entry = []
    with open(csv_file_path, 'r', newline='') as file:
        # Use DictReader to treat each row as a dictionary with column headers as keys
        reader = csv.DictReader(file)
        for row in reader:
            # Skip rows with empty name field
            if not row.get('Name', '').strip():
                continue
            if row['Name'] == name:
                entry.append(row)
                break

    return entry

def create_csv_file() -> None:
    os.makedirs(os.path.dirname(csv_file_path), exist_ok=True)
    with open(csv_file_path, "w", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Protein", "Fat", "Carbs", "Calories", "DateTime"])

def check_csv_file_exists() -> None:
    exists = False
    while not exists:
        try:
            with open(csv_file_path, "r") as file:
                exists = True
        except FileNotFoundError:
            create_csv_file()

#statistics functions
def get_daily_totals() -> list[dict[str, str | float]]:
    """Calculate daily totals for Protein, Fat, Carbs, Calories.
    
    Sums all nutrition values for the current day.
    
    Returns:
        Single-item list with totals, or None if no entries found
        
    Note:
        Gracefully handles malformed entries by skipping them
    """

    entries = get_entries_by_date()

    if not entries:
        return None

    # Initialize totals
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

    return [{
        'Name': 'Daily Total',
        'Protein': round(total_protein, 2), 
        'Fat': round(total_fat, 2), 
        'Carbs': round(total_carbs, 2), 
        'Calories': round(total_calories, 2)
        }]

def get_weekly_averages() -> list[dict[str, str | float]]:
    """Calculate weekly averages for Protein, Fat, Carbs, Calories.
    
    Averages all nutrition values from entries within the last 7 days.
    
    Returns:
        Single-item list with averages, or None if no entries found
        
    Note:
        Gracefully handles malformed entries by skipping them
    """
    entries = get_entries_within_week()

    if not entries:
        return None

    # Initialize totals
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
    
    # Calculate averages
    count = len(entries)
    return [{
        'Name': 'Weekly Average',
        'Protein': round(total_protein / count, 2),
        'Fat': round(total_fat / count, 2),
        'Carbs': round(total_carbs / count, 2),
        'Calories': round(total_calories / count, 2)
    }]