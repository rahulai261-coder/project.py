import csv
import os
from datetime import datetime
import pandas as pd


FILE_NAME = "expenses.csv"


def initialize_file():
    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Category", "Description", "Amount"])


# --------------------------------------------------
# Validate Date
# --------------------------------------------------
def validate_date(date_string):
    try:
        datetime.strptime(date_string, "%Y-%m-%d")
        return True
    except ValueError:
        return False


# --------------------------------------------------
# Add Expense
# --------------------------------------------------
def add_expense():
    print("\n--- Add Expense ---")

    date = input("Enter date (YYYY-MM-DD): ").strip()

    # Validate date
    if not validate_date(date):
        print("Invalid date. Please use YYYY-MM-DD format.")
        return

    category = input("Enter category: ").strip()

    if category == "":
        print("Category cannot be empty.")
        return

    description = input("Enter description: ").strip()

    # Validate amount
    try:
        amount = float(input("Enter amount: ").strip())

        if amount <= 0:
            print("Invalid amount. Amount must be a positive number. Expense not saved.")
            return

    except ValueError:
        print("Invalid amount. Amount must be a positive number. Expense not saved.")
        return

    # Save expense to CSV
    with open(FILE_NAME, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([
            date,
            category,
            description,
            amount
        ])

    # Count total records
    with open(FILE_NAME, "r") as file:
        reader = csv.DictReader(file)
        records = list(reader)

    print(f"Expense saved. Total records: {len(records)}")


# --------------------------------------------------
# View All Expenses
# --------------------------------------------------
def view_expenses():
    print("\n--- All Expenses ---")

    try:
        df = pd.read_csv(FILE_NAME)

        if df.empty:
            print("No expenses found.")
            return

        print(df.to_string(index=False))

    except FileNotFoundError:
        print("Expense file not found.")


# --------------------------------------------------
# Category-wise Summary
# --------------------------------------------------
def category_summary():
    print("\n--- Category-wise Summary ---")

    try:
        df = pd.read_csv(FILE_NAME)

        if df.empty:
            print("No expenses found.")
            return

        # Convert Amount to numeric
        df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")

        # Group expenses by Category
        summary = df.groupby("Category")["Amount"].sum()

        for category, amount in summary.items():
            print(f"{category}: {amount:g}")

        print(f"Total: {df['Amount'].sum():g}")

    except FileNotFoundError:
        print("Expense file not found.")


# --------------------------------------------------
# Search Expenses by Category
# --------------------------------------------------
def search_by_category():
    print("\n--- Search by Category ---")

    category = input("Enter category: ").strip()

    df = pd.read_csv(FILE_NAME)

    result = df[
        df["Category"].str.lower() == category.lower()
    ]

    if result.empty:
        print("No expenses found for this category.")
    else:
        print(result.to_string(index=False))


# --------------------------------------------------
# Main Menu
# --------------------------------------------------
def main():
    initialize_file()

    while True:
        print("\n================================")
        print("       PERSONAL EXPENSE TRACKER")
        print("================================")
        print("1. Add Expense")
        print("2. View All Expenses")
        print("3. Category-wise Summary")
        print("4. Search by Category")
        print("5. Exit")
        print("================================")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_expense()

        elif choice == "2":
            view_expenses()

        elif choice == "3":
            category_summary()

        elif choice == "4":
            search_by_category()

        elif choice == "5":
            print("Thank you for using Personal Expense Tracker.")
            break

        else:
            print("Invalid choice. Please select 1 to 5.")


# --------------------------------------------------
# Program Start
# --------------------------------------------------
if __name__ == "__main__":
    main()