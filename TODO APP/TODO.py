import json
from datetime import datetime

# Global variables
tasks = []
dark_mode = False
current_user = None

# Load tasks for a specific user
def load_tasks(filename="tasks.json"):
    global tasks
    try:
        with open(filename, "r") as file:
            tasks = json.load(file)
        print(f"Welcome back, {current_user}! Your tasks are loaded.")
    except FileNotFoundError:
        print(f"No tasks found for {current_user}. Starting fresh!")
    print()

# Save tasks for the current user
def save_tasks(filename="tasks.json"):
    with open(filename, "w") as file:
        json.dump(tasks, file)

# Add task
def add_task():
    title = input("Task title: ")
    description = input("Details (optional): ")
    priority = input("Priority (Low/Medium/High): ").capitalize()
    task = {
        "title": title,
        "description": description,
        "priority": priority,
        "completed": False,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    tasks.append(task)
    print(f"Task '{title}' added successfully!\n")

# View tasks
def view_tasks():
    if not tasks:
        print(f"No tasks available. Add something to get started!\n")
        return
    print(f"Here are your tasks, {current_user}:")
    for idx, task in enumerate(tasks, 1):
        status = "✅ Done" if task["completed"] else "🕒 Pending"
        print(f"{idx}. {task['title']} ({task['priority']}) - {status}")
        if task.get("description"):
            print(f"   - {task['description']}")
    print()

# Mark task as complete
def complete_task():
    view_tasks()
    try:
        task_num = int(input("Which task did you complete? (Enter number): "))
        tasks[task_num - 1]["completed"] = True
        print(f"Great work! Task marked as complete.\n")
    except (ValueError, IndexError):
        print(f"Invalid task number. Please try again.\n")

# Toggle dark mode
def toggle_dark_mode():
    global dark_mode
    dark_mode = not dark_mode
    if dark_mode:
        print(f"Dark mode activated!")
    else:
        print(f"Dark mode deactivated!")
    print()

# User selection
def switch_user():
    global current_user
    current_user = input("Enter your username: ")
    user_file = f"{current_user}_tasks.json"
    load_tasks(user_file)

# Main loop
def main():
    global current_user
    print(f"Welcome to the Collaborative To-Do List!")
    switch_user()

    while True:
        print(f"Menu:")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Complete Task")
        print("4. Toggle Dark Mode")
        print("5. Switch User")
        print("6. Exit")

        choice = input("What would you like to do? ")

        if choice == "1":
            add_task()
        elif choice == "2":
            view_tasks()
        elif choice == "3":
            complete_task()
        elif choice == "4":
            toggle_dark_mode()
        elif choice == "5":
            save_tasks(f"{current_user}_tasks.json")
            switch_user()
        elif choice == "6":
            save_tasks(f"{current_user}_tasks.json")
            print(f"Goodbye, {current_user}! Your tasks are saved.")
            break
        else:
            print(f"Invalid choice. Please try again.\n")

if __name__ == "__main__":
    main()
