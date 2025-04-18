  import json
from tkinter import Tk, Label, Entry, Button, Listbox, END, messagebox, StringVar, Toplevel, OptionMenu

# Public variables
tasks = []
current_user = None
task_file = None
dark_mode = False

# Save tasks to a file
def save_tasks():
    if task_file:
        with open(task_file, "w") as file:
            json.dump(tasks, file)

# Load tasks from a file
def load_tasks():
    global tasks
    try:
        with open(task_file, "r") as file:
            tasks[:] = json.load(file)
    except FileNotFoundError:
        tasks.clear()

# Update the task list in the GUI
def update_task_list():
    task_list.delete(0, END)
    for idx, task in enumerate(tasks):
        status = "✅" if task["completed"] else "🕒"
        task_list.insert(END, f"{idx + 1}. {task['title']} ({task['priority']}) - {status}")

def add_task():
    title = task_title_var.get().strip()
    priority = priority_var.get()
    if not title:
        messagebox.showwarning("Input Error", "Task title cannot be empty!")
        return
    task = {"title": title, "priority": priority, "completed": False}
    tasks.append(task)
    update_task_list()
    save_tasks()
    task_title_var.set("")
    priority_var.set("Low")

# Mark task as complete
def complete_task():
    selected = task_list.curselection()
    if not selected:
        messagebox.showwarning("Selection Error", "No task selected!")
        return
    idx = selected[0]
    tasks[idx]["completed"] = True
    update_task_list()
    save_tasks()

# Switch user function
def switch_user():
    global current_user, task_file
    username = username_var.get().strip()
    if not username:
        messagebox.showwarning("Input Error", "Username cannot be empty!")
        return
    current_user = username
    task_file = f"{current_user}_tasks.json"
    load_tasks()
    update_task_list()
    root.title(f"To-Do List - {current_user}")

# Toggle dark mode
def toggle_dark_mode():
    global dark_mode
    dark_mode = not dark_mode
    if dark_mode:
        root.configure(bg="black")
        for widget in root.winfo_children():
            widget.configure(bg="black", fg="white")
        task_list.configure(bg="black", fg="white")
        messagebox.showinfo("Dark Mode", "Dark mode activated!")
    else:
        root.configure(bg="white")
        for widget in root.winfo_children():
            widget.configure(bg="white", fg="black")
        task_list.configure(bg="white", fg="black")
        messagebox.showinfo("Dark Mode", "Dark mode deactivated!")

# GUI Setup
root = Tk()
root.title("To-Do List")
root.geometry("500x500")
root.configure(bg="white")

# Username input
username_var = StringVar()
Label(root, text="Username:", bg="white").pack(pady=5)
Entry(root, textvariable=username_var).pack(pady=5)
Button(root, text="Switch User", command=switch_user).pack(pady=10)

# Task input
task_title_var = StringVar()
priority_var = StringVar(value="Low")
Label(root, text="Task Title:", bg="white").pack(pady=5)
Entry(root, textvariable=task_title_var).pack(pady=5)
Label(root, text="Priority (Low/Medium/High):", bg="white").pack(pady=5)
OptionMenu(root, priority_var, "Low", "Medium", "High").pack(pady=5)
Button(root, text="Add Task", command=add_task).pack(pady=10)

# Task list
task_list = Listbox(root, width=50, height=15, bg="white", fg="black")
task_list.pack(pady=20)

# Buttons for actions
Button(root, text="Mark as Complete", command=complete_task).pack(pady=5)
Button(root, text="Toggle Dark Mode", command=toggle_dark_mode).pack(pady=5)

# Run the GUI
root.mainloop()
