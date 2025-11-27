import data
import ui
import datetime

def main() -> None:

    is_running = True
    while is_running:

        data.check_csv_file_exists()
        ui.show_main_menu()

        choice = ui.get_int_input("Enter your Choice: ")
        if choice == 1:
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

        elif choice == 2:
            ui.clear_terminal()
            recipe = ui.get_string_input("Enter the Name of the Recipe to use from the Nutrition Entries List: ")
            try:
                entry = data.get_entry_by_name(recipe)

            except FileNotFoundError as e:
                data.create_csv_file()
                ui.add_nutrition_failed(e)

            except ValueError as e:
                ui.add_nutrition_failed(e)

            # Only proceed if entry was found
            if entry:
                try:
                    data.write_nutrition_data((entry[0]["Name"], entry[0]["Protein"], entry[0]["Fat"], entry[0]["Carbs"], entry[0]["Calories"], datetime.datetime.now()))
                    ui.add_nutrition_successful()
                except FileNotFoundError as e:
                    data.create_csv_file()
                    ui.add_nutrition_failed(e)
            else:
                ui.add_nutrition_failed("Recipe Not Found in the Nutrition Entries List.")

        elif choice == 3:
            ui.clear_terminal()
            try:
                entries = data.get_all_entries()
                ui.show_stats_result(entries, "Nutrition Entries:", "No Entries Found.")
            except FileNotFoundError as e:
                data.create_csv_file()
                ui.show_entries_failed(e)
            except IndexError as e:
                ui.show_entries_failed(e)

        elif choice == 4:
            ui.clear_terminal()
            stats_running = True
            while stats_running:
                ui.show_statistics_menu()
                stats_choice = ui.get_int_input("Select Statistics Type: ")

                try:
                    if stats_choice == 1:
                        totals = data.get_daily_totals()
                        ui.show_stats_result(totals, "Daily Total Intake", "No Entries Found for Today")
                        stats_running = False  # Exit stats menu after showing result
                    elif stats_choice == 2:
                        averages = data.get_weekly_averages()
                        ui.show_stats_result(averages, "Weekly Average Intake", "No Entries Found for this Week")
                        stats_running = False  # Exit stats menu after showing result
                    elif stats_choice == 3:
                        ui.clear_terminal()
                        stats_running = False  # Back to main menu
                    else:
                        ui.invalid_choice()
                        # Loop continues, will show menu again

                except FileNotFoundError as e:
                    data.create_csv_file()
                    ui.show_entries_failed(e)
                    stats_running = False
                except IOError as e:
                    ui.show_entries_failed(e)
                    stats_running = False
                except ValueError as e:
                    ui.show_entries_failed(e)
                    stats_running = False

        elif choice == 5:
            is_running = False
            ui.exit_message()
            break

        else:
            ui.invalid_choice()

if __name__ == "__main__":
    main()
