# includes functions to display menus
# includes functions to show nutrition entries
# 

def showMainMenu():
    print("Welcome to the Nutrition Tracker!")
    print("1. Add Nutrition Entry")
    print("2. Use Recipe from the Nutrition Entry List")
    print("3. View Nutrition Entries")
    print("4. View Statistics")
    print("5. Exit")

def addNutritionSuccessfull():
    print("Nutrition data added successfully!")

def addNutritionFailed(error):
    print(f"Failed to add nutrition data: {error}")

def getNutritionInput(): 
    pass

def showStatistics():
    pass

def showEntries(entries, max_width=30):
    """
    entries: list of dicts with keys Name, Protein, Fat, Carbs, Calories, DateTime
    Prints a neat table to the console.
    """
    if not entries:
        print("No entries found.")
        return

    # Define columns and header order
    cols = ["Name", "Protein", "Fat", "Carbs", "Calories", "DateTime"]

    # Prepare rows as strings and compute column widths
    rows = []
    widths = {c: len(c) for c in cols}
    for e in entries:
        row = {}
        for c in cols:
            val = e.get(c, "")
            # Convert numeric-like values to string with no extra decimals
            if isinstance(val, float):
                s = f"{val:.2f}"
            else:
                s = str(val)
            # shorten long strings (like long names) for display
            if len(s) > max_width and c == "Name":
                s = s[: max_width - 3] + "..."
            row[c] = s
            widths[c] = max(widths[c], len(s))
        rows.append(row)

    # Build format string
    sep = " | "
    header = sep.join(c.ljust(widths[c]) for c in cols)
    divider = "-+-".join("-" * widths[c] for c in cols)

    # Print
    print(header)
    print(divider)
    for r in rows:
        print(sep.join(r[c].ljust(widths[c]) for c in cols))