import tkinter as tk
from tkinter import messagebox
import pickle
from datetime import datetime

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List App")
        self.root.geometry("400x400")  # Set window size
        self.root.configure(bg="#1e3d59")  # Set background color
        self.tasks = []
        self.load_tasks()

        # Task Entry
        self.task_entry = tk.Entry(root, width=40, bg="#d9bf77", fg="#1e3d59")  # Set entry box colors
        self.task_entry.grid(row=0, column=0, padx=10, pady=10)

        # Add Task Button
        add_button = tk.Button(root, text="Add Task", command=self.add_task, bg="#769fb6", fg="white")  # Set button colors
        add_button.grid(row=0, column=1, padx=10, pady=10)

        # Task Listbox
        self.task_listbox = tk.Listbox(root, height=15, width=50, bg="#d9bf77", fg="#1e3d59", selectbackground="#769fb6")  # Set listbox colors
        self.task_listbox.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        # Buttons for Remove and Mark Completed
        remove_button = tk.Button(root, text="Remove Task", command=self.remove_task, bg="#769fb6", fg="white")
        remove_button.grid(row=2, column=0, padx=10, pady=10, sticky="w")

        complete_button = tk.Button(root, text="Mark Completed", command=self.mark_completed, bg="#769fb6", fg="white")
        complete_button.grid(row=2, column=1, padx=10, pady=10, sticky="e")

        # Save and Exit Button
        save_button = tk.Button(root, text="Save and Exit", command=self.save_and_exit, bg="#e07a5f", fg="white")
        save_button.grid(row=3, column=0, columnspan=2, pady=10)

        self.update_task_list()

    def add_task(self):
        task_text = self.task_entry.get()
        if task_text:
            priority = self.get_priority()
            due_date = self.get_due_date()
            task = {"text": task_text, "priority": priority, "due_date": due_date, "completed": False}
            self.tasks.append(task)
            self.update_task_list()
            self.task_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Warning", "Task cannot be empty!")

    def remove_task(self):
        selected_index = self.task_listbox.curselection()
        if selected_index:
            self.tasks.pop(selected_index[0])
            self.update_task_list()
        else:
            messagebox.showwarning("Warning", "Select a task to remove!")

    def mark_completed(self):
        selected_index = self.task_listbox.curselection()
        if selected_index:
            self.tasks[selected_index[0]]["completed"] = True
            self.update_task_list()
        else:
            messagebox.showwarning("Warning", "Select a task to mark as completed!")

    def update_task_list(self):
        self.task_listbox.delete(0, tk.END)
        for task in self.tasks:
            status = "[ ]" if not task["completed"] else "[X]"
            priority = f"Priority: {task['priority']}"
            due_date = f"Due Date: {task['due_date']}" if task['due_date'] else ""
            self.task_listbox.insert(tk.END, f"{status} {task['text']} ({priority}, {due_date})")

    def get_priority(self):
        priority_window = tk.Toplevel(self.root)
        priority_window.title("Select Priority")

        priority_var = tk.StringVar(priority_window)
        priority_var.set("Medium")

        options = ["High", "Medium", "Low"]
        dropdown = tk.OptionMenu(priority_window, priority_var, *options)
        dropdown.pack()

        ok_button = tk.Button(priority_window, text="OK", command=priority_window.destroy)
        ok_button.pack()

        priority_window.wait_window(priority_window)

        return priority_var.get()

    def get_due_date(self):
        due_date_window = tk.Toplevel(self.root)
        due_date_window.title("Set Due Date")

        due_date_var = tk.StringVar(due_date_window)
        entry = tk.Entry(due_date_window, textvariable=due_date_var)
        entry.pack()

        ok_button = tk.Button(due_date_window, text="OK", command=due_date_window.destroy)
        ok_button.pack()

        due_date_window.wait_window(due_date_window)

        due_date_str = due_date_var.get()
        if due_date_str:
            try:
                due_date = datetime.strptime(due_date_str, "%Y-%m-%d").date()
                return due_date.strftime("%Y-%m-%d")
            except ValueError:
                messagebox.showwarning("Warning", "Invalid date format. Use YYYY-MM-DD.")
        return None

    def save_and_exit(self):
        with open("tasks.pkl", "wb") as file:
            pickle.dump(self.tasks, file)
        self.root.destroy()

    def load_tasks(self):
        try:
            with open("tasks.pkl", "rb") as file:
                self.tasks = pickle.load(file)
        except FileNotFoundError:
            pass

if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()
