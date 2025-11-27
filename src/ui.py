# includes functions to display menus
# includes functions to show nutrition entries
import os
import time

MAX_NAME_LENGTH = 30 

def show_main_menu() -> None:
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

def show_entries(entries: list, message: str) -> None:
    clear_terminal()
    if not entries:
        show_entries_failed("No Entries Found.")
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

def show_stats_result(result, title: str, empty_message: str) -> None:
    """Helper to display stats and a single corruption warning.

    - If `result` is truthy, shows entries with `title`.
    - Otherwise, shows `empty_message`.
    - Then scans CSV once and warns if corrupted rows were skipped.
    """
    if result:
        show_entries(result, title)
    else:
        show_entries_failed(empty_message)

    try:
        # Local import avoids potential circular-import issues at module load time
        import data  # type: ignore
        corrupt_count = data.scan_csv_for_corruption()
        if corrupt_count > 0:
            show_entries_failed(f"Warning: {corrupt_count} corrupted row(s) were skipped.")
    except IOError:
        pass

def show_entries_failed(error: str) -> None:
    clear_terminal()
    print(f"No Entries Found: {error}")
    time.sleep(2)

def add_nutrition_successful() -> None:
    clear_terminal()
    print("Nutrition Data Added Successfully!")
    time.sleep(1)

def add_nutrition_failed(error: str) -> None:
    clear_terminal()
    print(f"Failed to Add Nutrition Data: {error}")
    time.sleep(1)
    clear_terminal()

def invalid_choice() -> None:
    clear_terminal()
    print("Invalid Choice. Please Try Again.")
    time.sleep(1)
    clear_terminal()

def exit_message() -> None:
    clear_terminal()
    print("Exiting the Nutrition Tracker. Goodbye!")
    time.sleep(2)
    clear_terminal()

def get_string_input(message: str) -> str:  
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
    is_valid = False
    while not is_valid:
        try: 
            number = float(input(message))
            if number < 0:
                raise ValueError("Input Cannot be Negative.")
            is_valid = True
        except ValueError as e:
            print(f"Invalid Input. Please Enter a Valid Number. {e}")
    return number

def get_int_input(message: str) -> int:
    is_valid = False
    while not is_valid:
        try: 
            integer = int(input(message))
            if integer < 0:
                raise ValueError("Input Cannot be Negative.")
            is_valid = True
        except ValueError as e:
            print(f"Invalid Input. Please Enter a Valid Integer. {e}")
    return integer

def clear_terminal() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')