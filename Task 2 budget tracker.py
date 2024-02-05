import tkinter as tk
from tkinter import messagebox
from datetime import datetime

class BudgetTracker:
    def __init__(self, master):
        self.master = master
        self.master.title("Budget Tracker")

        # Initialize variables
        self.transactions = []
        self.current_balance = 0

        # Create GUI elements with color styling
        self.label_balance = tk.Label(master, text="Current Balance: $0.00", fg="green", font=("Helvetica", 14))
        self.label_balance.pack(pady=10)

        self.label_category = tk.Label(master, text="Category:", fg="blue")
        self.label_category.pack()

        self.entry_category = tk.Entry(master, width=20, borderwidth=2)
        self.entry_category.pack()

        self.label_amount = tk.Label(master, text="Amount:", fg="blue")
        self.label_amount.pack()

        self.entry_amount = tk.Entry(master, width=10, borderwidth=2)
        self.entry_amount.pack()

        self.button_income = tk.Button(master, text="Add Income", command=self.add_income, bg="green", fg="white")
        self.button_expense = tk.Button(master, text="Add Expense", command=self.add_expense, bg="red", fg="white")

        self.button_income.pack(pady=10)
        self.button_expense.pack()

        self.button_dashboard = tk.Button(master, text="Show Dashboard", command=self.show_dashboard, bg="blue", fg="white")
        self.button_history = tk.Button(master, text="Show Transaction History", command=self.show_history, bg="purple", fg="white")

        self.button_dashboard.pack(pady=10)
        self.button_history.pack()

    def add_income(self):
        self.add_transaction("Income")

    def add_expense(self):
        self.add_transaction("Expense")

    def add_transaction(self, transaction_type):
        category = self.entry_category.get()
        amount = self.entry_amount.get()

        if not category or not amount:
            messagebox.showwarning("Error", "Please enter both category and amount.")
            return

        try:
            amount = float(amount)
        except ValueError:
            messagebox.showwarning("Error", "Amount must be a valid number.")
            return

        if transaction_type == "Expense":
            amount *= -1

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.transactions.append({"timestamp": timestamp, "category": category, "amount": amount})

        self.current_balance += amount
        self.update_balance_label()

        self.entry_category.delete(0, tk.END)
        self.entry_amount.delete(0, tk.END)

        messagebox.showinfo("Success", f"{transaction_type} added successfully!")

    def update_balance_label(self):
        self.label_balance.config(text=f"Current Balance: ${self.current_balance:.2f}")

    def show_dashboard(self):
        total_income = sum(transaction['amount'] for transaction in self.transactions if transaction['amount'] > 0)
        total_expense = sum(transaction['amount'] for transaction in self.transactions if transaction['amount'] < 0)

        messagebox.showinfo("Dashboard", f"Total Income: ${total_income:.2f}\nTotal Expenses: ${-total_expense:.2f}")

    def show_history(self):
        history_text = "Transaction History:\n"
        for transaction in self.transactions:
            history_text += f"{transaction['timestamp']} - {transaction['category']}: ${transaction['amount']:.2f}\n"

        if not self.transactions:
            history_text += "No transactions yet."

        messagebox.showinfo("Transaction History", history_text)

if __name__ == "__main__":
    root = tk.Tk()
    budget_tracker = BudgetTracker(root)
    root.mainloop()
