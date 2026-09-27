import json
import os
import tkinter as tk
from datetime import datetime
from tkinter import messagebox, ttk

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class ExpenseTrackerApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")
        self.root.geometry("1000x600")
        self.root.minsize(800, 500)

        self.data_file = "expenses.json"
        self.expenses = self.load_data()

        self.setup_ui()
        self.refresh_data()

    # --- UI SETUP ---
    def setup_ui(self):
        # Main Grid Layout Configuration
        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(0, weight=1)

        # Left Panel (Inputs & Form)
        left_frame = ttk.Frame(self.root, padding=15)
        left_frame.grid(row=0, column=0, sticky="nsew")

        ttk.Label(
            left_frame, text="Add New Expense", font=("Helvetica", 14, "bold")
        ).pack(anchor="w", pady=(0, 15))

        # Date Field
        ttk.Label(left_frame, text="Date (YYYY-MM-DD):").pack(
            anchor="w", pady=(5, 0)
        )
        self.date_entry = ttk.Entry(left_frame)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.date_entry.pack(fill="x", pady=(0, 10))

        # Amount Field
        ttk.Label(left_frame, text="Amount ($):").pack(anchor="w", pady=(5, 0))
        self.amount_entry = ttk.Entry(left_frame)
        self.amount_entry.pack(fill="x", pady=(0, 10))

        # Category Field
        ttk.Label(left_frame, text="Category:").pack(anchor="w", pady=(5, 0))
        self.categories = [
            "Food",
            "Transport",
            "Utilities",
            "Entertainment",
            "Shopping",
            "Other",
        ]
        self.category_cb = ttk.Combobox(
            left_frame, values=self.categories, state="readonly"
        )
        self.category_cb.current(0)
        self.category_cb.pack(fill="x", pady=(0, 10))

        # Description Field
        ttk.Label(left_frame, text="Description:").pack(
            anchor="w", pady=(5, 0)
        )
        self.desc_entry = ttk.Entry(left_frame)
        self.desc_entry.pack(fill="x", pady=(0, 15))

        # Add Button
        add_btn = ttk.Button(
            left_frame, text="Add Expense", command=self.add_expense
        )
        add_btn.pack(fill="x", pady=(0, 10))

        # Delete Selected Button
        del_btn = ttk.Button(
            left_frame, text="Delete Selected", command=self.delete_expense
        )
        del_btn.pack(fill="x")

        # Right Panel (Tabs for Table and Graph Dashboard)
        right_frame = ttk.Frame(self.root, padding=10)
        right_frame.grid(row=0, column=1, sticky="nsew")
        right_frame.columnconfigure(0, weight=1)
        right_frame.rowconfigure(0, weight=1)

        self.notebook = ttk.Notebook(right_frame)
        self.notebook.grid(row=0, column=0, sticky="nsew")

        # Tab 1: Transaction Treeview
        self.tree_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.tree_tab, text="Transactions")
        self.setup_treeview()

        # Tab 2: Matplotlib Dashboard
        self.chart_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.chart_tab, text="Analytics Dashboard")
        self.setup_chart()

    def setup_treeview(self):
        self.tree_tab.columnconfigure(0, weight=1)
        self.tree_tab.rowconfigure(0, weight=1)

        columns = ("ID", "Date", "Category", "Amount", "Description")
        self.tree = ttk.Treeview(
            self.tree_tab, columns=columns, show="headings"
        )

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center")

        self.tree.column("ID", width=40)
        self.tree.column("Description", width=200)

        scrollbar = ttk.Scrollbar(
            self.tree_tab, orient="vertical", command=self.tree.yview
        )
        self.tree.configure(yscroll=scrollbar.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

    def setup_chart(self):
        self.chart_tab.columnconfigure(0, weight=1)
        self.chart_tab.rowconfigure(0, weight=1)

        # Embed Matplotlib Figure
        self.fig, self.ax = plt.subplots(figsize=(5, 4), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.chart_tab)
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")

    # --- DATA & STORAGE LOGIC ---
    def load_data(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, "r") as f:
                    return json.load(f)
            except Exception:
                return []
        return []

    def save_data(self):
        with open(self.data_file, "w") as f:
            json.dump(self.expenses, f, indent=4)

    def add_expense(self):
        date_str = self.date_entry.get().strip()
        amount_str = self.amount_entry.get().strip()
        category = self.category_cb.get()
        desc = self.desc_entry.get().strip()

        # Validation
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror(
                "Invalid Input", "Date must be in YYYY-MM-DD format."
            )
            return

        try:
            amount = float(amount_str)
            if amount <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror(
                "Invalid Input", "Amount must be a positive number."
            )
            return

        entry = {
            "id": len(self.expenses) + 1,
            "date": date_str,
            "category": category,
            "amount": amount,
            "description": desc if desc else "N/A",
        }

        self.expenses.append(entry)
        self.save_data()
        self.refresh_data()

        # Clear input fields
        self.amount_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)

    def delete_expense(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning(
                "Selection Error", "Please select an item to delete."
            )
            return

        item_values = self.tree.item(selected_item[0], "values")
        entry_id = int(item_values[0])

        self.expenses = [e for e in self.expenses if e["id"] != entry_id]

        # Re-index remaining IDs
        for idx, e in enumerate(self.expenses, 1):
            e["id"] = idx

        self.save_data()
        self.refresh_data()

    # --- RENDER REFRESH LOGIC ---
    def refresh_data(self):
        # Update Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        for e in self.expenses:
            self.tree.insert(
                "",
                "end",
                values=(
                    e["id"],
                    e["date"],
                    e["category"],
                    f"${e['amount']:.2f}",
                    e["description"],
                ),
            )

        # Update Chart
        self.update_chart()

    def update_chart(self):
        self.ax.clear()

        # Group amounts by category
        category_totals = {}
        for e in self.expenses:
            cat = e["category"]
            category_totals[cat] = category_totals.get(cat, 0) + e["amount"]

        if not category_totals:
            self.ax.text(
                0.5,
                0.5,
                "No data available to display",
                ha="center",
                va="center",
                fontsize=12,
            )
        else:
            categories = list(category_totals.keys())
            amounts = list(category_totals.values())

            # Draw Pie Chart
            self.ax.pie(
                amounts,
                labels=categories,
                autopct="%1.1f%%",
                startangle=140,
            )
            self.ax.set_title("Spending Breakdown by Category")

        self.fig.tight_layout()
        self.canvas.draw()


if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTrackerApp(root)
    root.mainloop()