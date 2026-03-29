tasks = []

def show_tasks():
    if not tasks:
        print("\n  No tasks yet!")
        return
    print("\n  Your Tasks:")
    print("  " + "-" * 30)
    for i, task in enumerate(tasks, 1):
        status = "✓" if task["done"] else "○"
        print(f"  {i}. [{status}] {task['name']}")
    print("  " + "-" * 30)
    done_count = sum(1 for t in tasks if t["done"])
    print(f"  {done_count}/{len(tasks)} completed")

def add_task():
    name = input("\n  Task name: ").strip()
    if not name:
        print("  Error: Task name cannot be empty!")
        return
    tasks.append({"name": name, "done": False})
    print(f"  ✅ Added: '{name}'")

def complete_task():
    show_tasks()
    if not tasks:
        return
    try:
        num = int(input("\n  Enter task number to mark complete: "))
        if 1 <= num <= len(tasks):
            if tasks[num - 1]["done"]:
                print(f"  Already completed: '{tasks[num - 1]['name']}'")
            else:
                tasks[num - 1]["done"] = True
                print(f"  ✅ Completed: '{tasks[num - 1]['name']}'")
        else:
            print("  Error: Invalid task number!")
    except ValueError:
        print("  Error: Please enter a valid number!")

def delete_task():
    show_tasks()
    if not tasks:
        return
    try:
        num = int(input("\n  Enter task number to delete: "))
        if 1 <= num <= len(tasks):
            removed = tasks.pop(num - 1)
            print(f"  🗑️  Deleted: '{removed['name']}'")
        else:
            print("  Error: Invalid task number!")
    except ValueError:
        print("  Error: Please enter a valid number!")

def clear_completed():
    before = len(tasks)
    tasks[:] = [t for t in tasks if not t["done"]]
    removed = before - len(tasks)
    if removed == 0:
        print("\n  No completed tasks to clear!")
    else:
        print(f"\n  🗑️  Cleared {removed} completed task(s)!")

# Main loop
print("=" * 35)
print("       📝 TO-DO LIST APP")
print("=" * 35)

while True:
    print("\n  1. View tasks")
    print("  2. Add task")
    print("  3. Mark complete")
    print("  4. Delete task")
    print("  5. Clear completed")
    print("  6. Exit")

    choice = input("\n  Choose (1-6): ").strip()

    if choice == "1":
        show_tasks()
    elif choice == "2":
        add_task()
    elif choice == "3":
        complete_task()
    elif choice == "4":
        delete_task()
    elif choice == "5":
        clear_completed()
    elif choice == "6":
        print("\n  Goodbye! 👋")
        break
    else:
        print("  Error: Please choose between 1 and 6!")
