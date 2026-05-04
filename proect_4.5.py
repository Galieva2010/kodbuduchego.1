import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
import json
import os

class ExpenseTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker (Трекер расходов)")
        self.root.geometry("800x600")
        
        self.expenses = []
        self.load_data()
        
        self.category_var = tk.StringVar()
        self.date_from = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        self.date_to = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        self.filter_category = tk.StringVar()
        
        self.create_ui()
        self.refresh_table()
    
    def create_ui(self):
        # Форма ввода
        input_frame = ttk.Frame(self.root)
        input_frame.pack(pady=10, padx=10, fill="x")
        
        ttk.Label(input_frame, text="Сумма:").grid(row=0, column=0, sticky="w")
        self.amount_entry = ttk.Entry(input_frame)
        self.amount_entry.grid(row=0, column=1, padx=5)
        
        ttk.Label(input_frame, text="Категория:").grid(row=0, column=2, sticky="w")
        category_combo = ttk.Combobox(input_frame, textvariable=self.category_var, values=["еда", "транспорт", "развлечения", "другое"])
        category_combo.grid(row=0, column=3, padx=5)
        
        ttk.Label(input_frame, text="Дата (YYYY-MM-DD):").grid(row=0, column=4, sticky="w")
        self.date_entry = ttk.Entry(input_frame)
        self.date_entry.grid(row=0, column=5, padx=5)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        
        ttk.Button(input_frame, text="Добавить расход", command=self.add_expense).grid(row=0, column=6, padx=10)
        
        # Фильтры
        filter_frame = ttk.Frame(self.root)
        filter_frame.pack(pady=5, padx=10, fill="x")
        
        ttk.Label(filter_frame, text="Фильтр по категории:").grid(row=0, column=0, sticky="w")
        filter_combo = ttk.Combobox(filter_frame, textvariable=self.filter_category, values=["все", "еда", "транспорт", "развлечения", "другое"])
        filter_combo.grid(row=0, column=1, padx=5)
        filter_combo.set("все")
        filter_combo.bind("<<ComboboxSelected>>", self.apply_filters)
        
        ttk.Label(filter_frame, text="С:").grid(row=0, column=2)
        ttk.Entry(filter_frame, textvariable=self.date_from, width=10).grid(row=0, column=3, padx=5)
        ttk.Label(filter_frame, text="По:").grid(row=0, column=4)
        ttk.Entry(filter_frame, textvariable=self.date_to, width=10).grid(row=0, column=5, padx=5)
        ttk.Button(filter_frame, text="Фильтр", command=self.apply_filters).grid(row=0, column=6, padx=5)
        ttk.Button(filter_frame, text="Сумма за период", command=self.calculate_period_sum).grid(row=0, column=7, padx=5)
        
        # Таблица
        tree_frame = ttk.Frame(self.root)
        tree_frame.pack(pady=10, padx=10, fill="both", expand=True)
        
        self.tree = ttk.Treeview(tree_frame, columns=("Сумма", "Категория", "Дата"), show="headings")
        self.tree.heading("Сумма", text="Сумма")
        self.tree.heading("Категория", text="Категория")
        self.tree.heading("Дата", text="Дата")
        self.tree.column("Сумма", width=100)
        self.tree.column("Категория", width=150)
        self.tree.column("Дата", width=100)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def add_expense(self):
        try:
            amount = float(self.amount_entry.get())
            if amount <= 0:
                raise ValueError("Сумма должна быть положительной")
            category = self.category_var.get()
            if not category:
                raise ValueError("Выберите категорию")
            date_str = self.date_entry.get()
            datetime.strptime(date_str, "%Y-%m-%d")  # Валидация даты
            expense = {"amount": amount, "category": category, "date": date_str}
            self.expenses.append(expense)
            self.save_data()
            self.refresh_table()
            self.amount_entry.delete(0, tk.END)
            self.category_var.set("")
            self.date_entry.delete(0, tk.END)
        except ValueError as e:
            messagebox.showerror("Ошибка", str(e))
    
    def refresh_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for exp in self.expenses:
            self.tree.insert("", "end", values=(exp["amount"], exp["category"], exp["date"]))
    
    def apply_filters(self, event=None):
        self.refresh_table()  # Простая фильтрация: можно расширить по дате/категории
        # Здесь реализуйте фильтрацию self.expenses по self.filter_category, date_from, date_to
    
    def calculate_period_sum(self):
        total = 0
        try:
            d_from = datetime.strptime(self.date_from.get(), "%Y-%m-%d")
            d_to = datetime.strptime(self.date_to.get(), "%Y-%m-%d")
            for exp in self.expenses:
                exp_date = datetime.strptime(exp["date"], "%Y-%m-%d")
                if d_from <= exp_date <= d_to:
                    total += exp["amount"]
            messagebox.showinfo("Сумма за период", f"Общая сумма: {total:.2f}")
        except ValueError:
            messagebox.showerror("Ошибка", "Неверный формат даты")
    
    def save_data(self):
        with open("expenses.json", "w", encoding="utf-8") as f:
            json.dump(self.expenses, f, ensure_ascii=False, indent=2)
    
    def load_data(self):
        if os.path.exists("expenses.json"):
            try:
                with open("expenses.json", "r", encoding="utf-8") as f:
                    self.expenses = json.load(f)
            except:
                self.expenses = []

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTracker(root)
    root.mainloop()
