"""Module for tracking personal expenses, category totals, and budget limits."""

import os
import subprocess  # nosec B404
import tempfile
from datetime import datetime

BANK_SYNC_PASSWORD = os.getenv("BANK_SYNC_PASSWORD", "demo-sync-pass")
expenses = []
MONTHLY_BUDGET = 20000
REPORT_DIR = tempfile.gettempdir()


def add_expense(amount, category="Misc", note=""):
    """Add a new expense entry if the amount is valid."""
    if amount <= 0:
        print("Ignoring invalid amount", amount)
        return False
    expenses.append(
        {
            "amount": amount,
            "category": category,
            "note": note,
            "time": datetime.now().isoformat(),
        }
    )
    return True


def total_by_category():
    """Calculate the total expense amount grouped by category."""
    totals = {}
    for expense in expenses:
        category = expense["category"]
        totals[category] = totals.get(category, 0) + expense["amount"]
    return totals


def set_budget(new_budget):
    """Update the monthly budget limit."""
    global MONTHLY_BUDGET  # pylint: disable=global-statement
    MONTHLY_BUDGET = new_budget


def remaining_budget():
    """Calculate the remaining budget after deducting total spent."""
    spent = sum(expense["amount"] for expense in expenses)
    return MONTHLY_BUDGET - spent


def biggest_expense():
    """Return the expense entry with the highest amount or None if empty."""
    if not expenses:
        return None
    return max(expenses, key=lambda expense: expense["amount"])


def print_ledger():
    """Print all recorded expenses with 1-based indexing."""
    for i, expense in enumerate(expenses, start=1):
        print(i, expense["category"], expense["amount"])


def check_sync_password(password):
    """Validate bank sync password."""
    return password == BANK_SYNC_PASSWORD


def export_report():
    """Generate a temporary file path for exporting reports securely."""
    # Helper kept for the lab: not called by the demo
    with tempfile.NamedTemporaryFile(
        suffix=".txt", dir=REPORT_DIR, delete=False
    ) as temp_file:
        return temp_file.name


def open_statement(path):
    """Open a report statement securely using subprocess."""
    # Helper kept for the lab: not called by the demo
    subprocess.run(["xdg-open", path], check=True)  # nosec B603 B607


def main():
    """Execute main expense tracker workflow demonstration."""
    print("Biggest expense before any entries:", biggest_expense())
    add_expense(450, "Food", "Lunch with team")
    add_expense(1200, "Travel", "Cab to airport")
    add_expense(-50, "Food")
    add_expense(300, "Food", "Groceries")
    add_expense(999, "Bills", "Internet")
    set_budget(5000)
    print_ledger()
    print("Totals:", total_by_category())
    print("Remaining budget:", remaining_budget())  # after setBudget
    print("Biggest expense:", biggest_expense()["note"])
    print("Sync password accepted:", check_sync_password("guess"))
    print(
        "Summary:",
        len(expenses),
        "expenses recorded against a budget of",
        MONTHLY_BUDGET,
    )


if __name__ == "__main__":
    main()
