import csv
import os
from datetime import datetime

FILENAME = "expenses.csv"

def initialize_csv():
    """Create CSV file with headers if it doesn't exist"""
    if not os.path.exists(FILENAME):
        with open(FILENAME, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Date', 'Category', 'Amount (Rs)', 'Note'])

def load_expenses():
    """Load all expenses from CSV"""
    expenses = []
    if os.path.exists(FILENAME):
        with open(FILENAME, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                expenses.append(row)
    return expenses

def add_expense():
    """Add expense and save to CSV"""
    date = input("Enter date (YYYY-MM-DD) [press Enter for today]: ").strip()
    if not date:
        date = datetime.now().strftime("%Y-%m-%d")
    category = input("Enter category (e.g., Food, Travel, Books): ").strip()
    if not category:
        print("Category cannot be empty!")
        return
    try:
        amount = float(input("Enter amount (Rs): "))
    except ValueError:
        print("Invalid amount! Please enter a number.")
        return
    note = input("Enter note (optional): ").strip()
    with open(FILENAME, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([date, category, amount, note])
    print("✓ Expense added successfully!")

def view_expenses():
    """Display all expenses from CSV"""
    expenses = load_expenses()
    if not expenses:
        print("No expenses recorded.")
        return
    print("\n--- All Expenses ---")
    print(f"{'No.':<4} {'Date':<12} {'Category':<15} {'Amount (Rs)':<12} {'Note':<20}")
    print("-" * 65)
    for idx, exp in enumerate(expenses, 1):
        date = exp.get('Date', '')
        category = exp.get('Category', '')
        amount = exp.get('Amount (Rs)', '')
        note = exp.get('Note', '')[:18]  # Truncate long notes
        print(f"{idx:<4} {date:<12} {category:<15} {amount:<12} {note:<20}")

def delete_expense():
    """Delete expense by index"""
    expenses = load_expenses()
    if not expenses:
        print("No expenses to delete.")
        return
    view_expenses()
    try:
        idx = int(input("\nEnter the number of the expense to delete: ")) - 1
        if 0 <= idx < len(expenses):
            with open(FILENAME, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Date', 'Category', 'Amount (Rs)', 'Note'])
                for i, exp in enumerate(expenses):
                    if i != idx:
                        writer.writerow([exp['Date'], exp['Category'], exp['Amount (Rs)'], exp['Note']])
            print(f"✓ Deleted: {expenses[idx]}")
        else:
            print("Invalid index!")
    except ValueError:
        print("Invalid input!")

def show_summary():
    """Show spending summary from CSV"""
    expenses = load_expenses()
    if not expenses:
        print("No expenses to summarize.")
        return
    try:
        total = sum(float(exp.get('Amount (Rs)', 0)) for exp in expenses)
        print(f"\n--- Spending Summary ---")
        print(f"Total spent: Rs {total:.2f}")
        # Category wise summary
        categories = {}
        for exp in expenses:
            cat = exp.get('Category', 'Uncategorized')
            amt = float(exp.get('Amount (Rs)', 0))
            categories[cat] = categories.get(cat, 0) + amt
        print("\nBy category:")
        for cat in sorted(categories.keys(), key=lambda x: categories[x], reverse=True):
            amt = categories[cat]
            print(f"  • {cat}: Rs {amt:.2f}")
    except ValueError:
        print("Error calculating summary!")

def main():
    """Main menu loop"""
    initialize_csv()
    while True:
        print("\n--- Personal Expense Tracker ---")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Delete Expense")
        print("4. Show Summary")
        print("5. Exit")
        choice = input("Select an option: ").strip()
        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            delete_expense()
        elif choice == "4":
            show_summary()
        elif choice == "5":
            print("Bye! Your data is saved in expenses.csv")
            break
        else:
            print("Invalid input. Try again.")

if __name__ == "__main__":
    main()
