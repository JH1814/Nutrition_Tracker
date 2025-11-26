# Nutrition Tracker
## Problem
Many people track their daily nutrition manually using notes or spreadsheets, which often leads to **input errors, missing data**, and **no automatic** daily summaries.
A console-based tracker can simplify this process by storing entries in a structured format and generating quick overviews.

## Scenario
A user opens the program daily to record food items they’ve eaten — including date, category (e.g., protein, fat, carbs, sugar), and amount.
The program validates the inputs, saves them into a file, and allows users to view summaries like total calories or nutrients per day or week.

## User Stories
1.	As a user, I want to **add food entries** with date, category, and quantity so I can track my nutrition.

2.	As a user, I want to **get a list of all entries** to have a full overview about what I ate.

3.	As a user, I want to **view my daily and weekly totals** to understand my intake.

4.	As a user, I want my data to be **saved and loaded automatically**, so I don’t lose progress.

5.	As a user, I want to be notified when I enter **invalid data** (e.g., wrong date or negative amount).

## Use Cases
* **Add Entry:** User inputs a new nutrition record.
* **List Entries:** Display all or filtered records.
* **Show Statistics:** Calculate and display daily or weekly totals.
* **Save / Load Entries:** Store and retrieve entries from a file (.json or .csv).
* **Exit:** Safely quit the program.

## Project Requirements
### Each project must fulfill these three conditions:
1.	**Interactive App (console input)**
2.	**Data validation (input checking)**
3.	**File processing (read/write)**






## Filestructure  

Our project uses the **MVC structure (Model - View - Controller)**.  
This structure helps to keep the code clean, organized, and easy to maintain.

### Model
The Model handles all data operations.  
It reads and writes data from the `data.csv` file and contains the main program logic such as calculations and data validation.

### View
The View is responsible for displaying information to the user.  
It shows menus, messages, and outputs in the console.

### Controller
The Controller manages the connection between the Model and the View.  
It receives user input, decides what to do, and coordinates actions between data and output.

### main.py
The `main.py` file is the entry point of the program.  
It starts the Controller and connects all parts of the application.

### data.csv
The `data.csv` file stores all saved user data.  
It is used by the Model for loading and saving information.





## 🧩 User Manual

The following section explains step-by-step how to use the **Nutrition Tracker** application.

---

### 1️⃣ Start the Program

When you start the program, the **main menu** will appear in your terminal.

Example:
```
Welcome to Nutrition Tracker!

1. Add a new food entry
2. View all entries
3. View entries of the current week
4. Show statistics
5. Exit program
```

➡️ Choose an option by typing the number (1–5) and pressing **Enter**.

---

### 2️⃣ Add a New Food Entry

Select option **1** from the main menu.  
The program will ask you to enter information about your meal.

Example prompt:
```
Food name: 
Calories: 
Date (YYYY-MM-DD):
```

Example input:
```
Food name: Pizza
Calories: 850
Date: 2025-11-04
```

✅ If all inputs are valid, your entry will be saved successfully.  
❌ If you enter invalid data (like empty text or wrong number format), the program will show an error message and ask again.

---

### 3️⃣ View All Entries

Select option **2** from the main menu.  
This will display all entries currently saved in the system.

Example output:
```
1. Pizza – 850 kcal – 2025-11-04
2. Salad – 300 kcal – 2025-11-04
3. Pasta – 700 kcal – 2025-11-05
```

➡️ Use this option to quickly see what you have eaten and how many calories you recorded.

---

### 4️⃣ View Entries from the Current Week

Select option **3** from the main menu.  
This will show all entries recorded **within the last 7 days** and also calculate the **total calories of the week**.

Example output:
```
Entries from this week:
- Pizza (850 kcal)
- Salad (300 kcal)
- Pasta (700 kcal)
Total calories this week: 1850 kcal
```

➡️ Use this to check your weekly calorie balance and track your eating habits.

---

### 5️⃣ Show Statistics

Select option **4** from the main menu.  
The program will display simple statistics based on your stored data.

Example output:
```
--- Weekly Statistics ---
Average calories/day: 925 kcal
Highest entry: Pizza (850 kcal)
Lowest entry: Salad (300 kcal)
```

➡️ This helps you analyze your nutrition over time.

---

### 6️⃣ Exit the Program

Select option **5** to close the program.  
All your data will be saved automatically before the application exits.

Example:
```
Exiting program...
Goodbye!
```

➡️ Always use this option to ensure your data is stored correctly before closing the program.

---

### ✅ Summary of Menu Options

| Option | Description |
|:--:|:--|
| 1 | Add a new food entry |
| 2 | View all entries |
| 3 | View entries of the current week |
| 4 | Show weekly statistics |
| 5 | Exit the program |

---

### 🧠 Tips

- Always enter numbers (calories) without extra spaces or letters.  
- Dates must follow the format `YYYY-MM-DD` (for example: `2025-11-04`).  
- If the program displays an error, just follow the message and re-enter the correct value.  
- Use lowercase “yes” / “no” when the program asks for a confirmation (if implemented).  

---

Enjoy tracking your meals and managing your daily calories with the **Nutrition Tracker**! 🍎
