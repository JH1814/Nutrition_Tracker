"""Main entry point for the Nutrition Tracker application.

Orchestrates user interaction by routing menu choices to appropriate handlers.
Each handler function manages a specific user operation (add, view, statistics, etc.).
"""
import data
import ui
import datetime
import import_ipynb
import visualization


def handle_add_entry() -> None:
    """Handle menu choice 1: Add a new nutrition entry.
    
    Prompts user for nutrition information and saves to CSV.
    """
    ui.clear_terminal()
    name = ui.get_string_input("Add Name of Nutrition Entry: ")
    protein = ui.get_float_input("Add Protein in grams: ")
    fat = ui.get_float_input("Add Fat in grams: ")
    carbs = ui.get_float_input("Add Carbs in grams: ")
    calories = ui.get_float_input("Add Calories in kcal: ")

    try:
        data.write_nutrition_data([name, protein, fat, carbs, calories, datetime.datetime.now()])
        ui.add_nutrition_successful()
    except FileNotFoundError as e:
        data.create_csv_file()
        ui.add_nutrition_failed(e)


def handle_reuse_entry() -> None:
    """Handle menu choice 2: Reuse an existing nutrition entry.
    
    Searches for entry by name and creates a new timestamped copy.
    """
    ui.clear_terminal()
    name = ui.get_string_input("Enter the Name of the Recipe to use from the Nutrition Entries List: ")
    
    try:
        entry = data.get_entry_by_name(name)
    except FileNotFoundError as e:
        data.create_csv_file()
        ui.add_nutrition_failed(e)
        return
    except ValueError as e:
        ui.add_nutrition_failed(e)
        return

    # Only proceed if entry was found
    if entry:
        try:
            data.write_nutrition_data([
                entry[0]["Name"], 
                entry[0]["Protein"], 
                entry[0]["Fat"], 
                entry[0]["Carbs"], 
                entry[0]["Calories"], 
                datetime.datetime.now()
            ])
            ui.add_nutrition_successful()
        except FileNotFoundError as e:
            data.create_csv_file()
            ui.add_nutrition_failed(e)
    else:
        ui.add_nutrition_failed("Recipe Not Found in the Nutrition Entries List.")


def handle_view_entries() -> None:
    """Handle menu choice 3: View all nutrition entries.
    
    Retrieves and displays all entries from the CSV file.
    """
    ui.clear_terminal()
    try:
        entries = data.get_all_entries()
        ui.show_entries(entries, "Nutrition Entries:", "No Entries Found.")
    except FileNotFoundError as e:
        data.create_csv_file()
        ui.format_entries_failed(e)
    except IndexError as e:
        ui.format_entries_failed(e)


def handle_statistics() -> None:
    """Handle menu choice 4: View statistics submenu.
    
    Displays statistics submenu and processes daily/weekly calculations.
    """
    ui.clear_terminal()
    stats_running = True
    
    while stats_running:
        ui.show_statistics_menu()
        stats_choice = ui.get_int_input("Select Statistics Type: ", max_value=4)

        try:
            if stats_choice == 1:
                totals = data.get_daily_totals()
                ui.show_entries(totals, "Daily Total Intake", "No Entries Found for Today")
                stats_running = False
            elif stats_choice == 2:
                averages = data.get_weekly_averages()
                ui.show_entries(averages, "Weekly Average Intake", "No Entries Found for this Week")
                stats_running = False
            elif stats_choice == 3:
                visualization.create_nutrition_graph()
                stats_running = False
            elif stats_choice == 4:
                ui.clear_terminal()
                stats_running = False
            else:
                ui.invalid_choice()

        except FileNotFoundError as e:
            data.create_csv_file()
            ui.format_entries_failed(e)
            stats_running = False
        except IOError as e:
            ui.format_entries_failed(e)
            stats_running = False
        except ValueError as e:
            ui.format_entries_failed(e)
            stats_running = False


def handle_exit() -> bool:
    """Handle menu choice 5: Exit the application.
    
    Returns:
        False to signal main loop should terminate
    """
    ui.exit_message()
    return False


def main() -> None:
    """Main application loop.
    
    Displays menu, gets user choice, and dispatches to appropriate handler.
    """
    is_running = True
    
    # Handler function mapping for clean dispatch
    handlers = {
        1: handle_add_entry,
        2: handle_reuse_entry,
        3: handle_view_entries,
        4: handle_statistics
    }
    
    while is_running:
        data.check_csv_file_exists()
        ui.show_main_menu()
        choice = ui.get_int_input("Enter your Choice: ", max_value=5)
        
        if choice == 5:
            is_running = handle_exit()
        elif choice in handlers:
            handlers[choice]()
        else:
            ui.invalid_choice()

if __name__ == "__main__":
    main()
