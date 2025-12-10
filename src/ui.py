"""User interface module for the Nutrition Tracker application.

Provides terminal-based menus, input validation, and display functions
for interacting with nutrition data.
"""
import os
import time
import data

# Validation constants
MAX_NAME_LENGTH: int = 30
MAX_NUMERIC_VALUE: float = 10000.0  # Reasonable upper limit for nutrition values 

def show_main_menu() -> None:
    """Display the main menu with all available options."""
    clear_terminal()
    print("Welcome to the Nutrition Tracker!")
    print("1. Add Nutrition Entry")
    print("2. Use Existing Nutrition Entry")
    print("3. View Nutrition Entries")
    print("4. View Statistics")
    print("5. Exit")

def show_statistics_menu() -> None:
    clear_terminal()
    print("Statistics Menu:")
    print("1. Daily Totals")
    print("2. Weekly Averages")
    print("3. Back to Main Menu")

def format_entries(entries: list[dict[str, str | float]], message: str) -> None:
    """Display nutrition entries in a formatted table.
    
    Args:
        entries: List of nutrition entry dictionaries
        message: Header message to display above the table
    """
    clear_terminal()
    if not entries:
        format_entries_failed("No Entries Found.")
        return

    print(message)
    # create header
    headers = ["Name", "Protein ", "Fat", "Carbs", "Calories"]
    print(f"{headers[0]:<30} {headers[1]:<10} {headers[2]:<10} {headers[3]:<10} {headers[4]:<10}")
    print("-" * 80)

    for entry in entries:
        name = entry.get('Name', '')
        protein = f"{entry.get('Protein', '')}g"
        fat = f"{entry.get('Fat', '')}g"
        carbs = f"{entry.get('Carbs', '')}g"
        calories = f"{entry.get('Calories', '')} kcal"
        print(f"{name:<30} {protein:<10} {fat:<10} {carbs:<10} {calories:<10}")
    
    input("\nPress Enter to continue...")
    clear_terminal()

def show_entries(result: list[dict[str, str | float]], title: str, empty_message: str) -> None:
    """Helper to display stats and a single corruption warning.

    - If `result` is truthy, shows entries with `title`.
    - Otherwise, shows `empty_message`.
    - Then scans CSV once and warns if corrupted rows were skipped.
    """
    if result:
        format_entries(result, title)
    else:
        format_entries_failed(empty_message)

    try:
        corrupt_count = data.scan_csv_for_corruption()
        if corrupt_count > 0:
            format_entries_failed(f"Warning: {corrupt_count} corrupted row(s) were skipped.")
    except IOError:
        pass

def format_entries_failed(error: str) -> None:
    # Do not clear immediately; show consistent error prefix so users can read
    print(f"Error: No Entries Found. Details: {error}")
    time.sleep(2)

def add_nutrition_successful() -> None:
    clear_terminal()
    print("Nutrition Data Added Successfully!")
    time.sleep(1)

def add_nutrition_failed(error: str) -> None:
    # Do not clear immediately; show consistent error prefix
    print(f"Error: Failed to Add Nutrition Data. Details: {error}")
    time.sleep(2)

def invalid_choice() -> None:
    # Do not clear immediately; show consistent error prefix
    print("Error: Invalid Choice. Please Try Again.")
    time.sleep(2)

def exit_message() -> None:
    clear_terminal()
    print("Exiting the Nutrition Tracker. Goodbye!")
    time.sleep(2)
    clear_terminal()

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

def get_int_new(msg:str, err_msg:str, min_val:int=None, max_val:int=None) -> int:
    """Get validated integer input from user within a specified range.
    
    Args:
        msg: Prompt message to display
        err_msg: Error message to display on invalid input
        min_val: Minimum acceptable integer value
        max_val: Maximum acceptable integer value
    """
    user_in = input(msg)
    try:
        user_int = int(user_in)
        if (min_val is not None and user_int < min_val) or (max_val is not None and user_int > max_val):
            raise ValueError(f"Input Out of Range. ({min_val})")
        return user_int
    except ValueError:
        print(err_msg)
        return get_int_new(msg, err_msg, min_val, max_val)

        

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

def clear_terminal() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')