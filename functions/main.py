import json
from datetime import datetime
from datetime import datetime, timedelta  # ✅ Ensure timedelta is imported

# ----- Core Task Functions -----
def add_burdens(tasks, daily_tasks):
    """Prompt user to add multiple tasks in one input."""
    print("\nBULK TASK ENTRY:")
    print("\nCATEGORIES: Urgent & Important, Not Urgent but Important, Urgent but Not Important, Not Urgent & Not Important")
    print("\nFORMAT AS: DESCRIPTION, CATEGORY, DATE (YYYY-MM-DD), TIME (HH:MM AM/PM), DURATION (e.g., 2h 30m))")
    print("\nSEPARATE YOUR BURDENS WITH ';'")

    user_input = input("\nENTER BURDENS: ").strip()
    task_entries = user_input.split(";")
    
    valid_categories = {c.lower(): c for c in tasks.keys()}  # Allow case-insensitive matching
    task_added = False  # 🔥 Track if at least one task was added

    for entry in task_entries:
        parts = [p.strip() for p in entry.split(",")]

        if len(parts) != 5:
            print(f"\n⚠️ INVALID FORMAT FOR: {entry}")
            print("REFRAME YOUR INTENT, MORTAL!")
            continue

        description, category, date, time, duration = parts
        category = valid_categories.get(category.lower())

        if not category:
            print(f"\n⚠️ INVALID CATEGORY ENTRY: {category}")
            print("REFRAME YOUR INTENT, MORTAL!")
            continue

        # ✅ Validate date format
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            print(f"\n⚠️ INVALID DATE FORMAT FOR: {date}")
            print("REFRAME YOUR INTENT, MORTAL!")
            continue

        # ✅ Validate time format
        try:
            datetime.strptime(time, "%I:%M %p")
        except ValueError:
            print(f"\n⚠️ INVALID TIME FORMAT FOR: {time}")
            print("REFRAME YOUR INTENT, MORTAL!")
            continue

        # ✅ Validate duration format
        if not any(char.isdigit() for char in duration):
            print(f"\n⚠️ INVALID DURATION FORMAT FOR: {duration}")
            print("REFRAME YOUR INTENT, MORTAL!")
            continue

        # ✅ Convert time to 24-hour format for sorting
        time_parts = time.split(" ")  # Splits "8:00 AM" -> ["8:00", "AM"]
        hour_minute = time_parts[0].split(":")  # Splits "8:00" -> ["8", "00"]
        hour, minute = int(hour_minute[0]), int(hour_minute[1])
        am_pm = time_parts[1]

        start_hour, start_minute = convert_to_24h(hour, minute, am_pm)
        start_time_24h = start_hour * 60 + start_minute  # Convert to minutes for comparison

        # ✅ Convert duration to total minutes
        duration_minutes = convert_duration_to_minutes(duration)

        # ✅ Check for overlapping tasks
        conflict = False
        for task in tasks[category]:
            task_time_parts = task['start_time'].split(" ")
            task_hour_minute = task_time_parts[0].split(":")
            existing_hour, existing_minute = int(task_hour_minute[0]), int(task_hour_minute[1])
            existing_am_pm = task_time_parts[1]

            existing_start_hour, existing_start_minute = convert_to_24h(existing_hour, existing_minute, existing_am_pm)
            existing_start_time = existing_start_hour * 60 + existing_start_minute
            existing_duration = convert_duration_to_minutes(task['duration'])
            existing_end_time = existing_start_time + existing_duration

            new_end_time = start_time_24h + duration_minutes

            if start_time_24h < existing_end_time and new_end_time > existing_start_time:
                print(f"⚠️ OVERLAPPING BURDENS: '{description}' conflicts with '{task['description']}' ({task['start_time']})")
                conflict = True
                break
        
        # ✅ Allow user to override the conflict warning
        if conflict:
            override = input("WILL YOU ADD THIS BURDEN REGARDLESS? (YES/NO): ").strip().lower()
            if override != "yes":
                print(f"BURDEN '{description}' NOT ADDED DUE TO CONFLICT.")
                continue

        # ✅ Ask if the task is recurring **AFTER all data is validated**
        is_recurring = input(f"\nIS '{description}' A RECURRING DAILY BURDEN? (YES/NO): ").strip().lower() == "yes"

        task_data = {
            "description": description,
            "category": category,  # ✅ Store the category so it doesn't default later
            "date": date,
            "start_time": time,
            "duration": duration
        }

        if is_recurring:
            daily_tasks.append(task_data)  # ✅ Store in `daily_tasks`
            print(f"\n🔄 RECURRING BURDEN '{description}' ADDED ({time}, {duration})")
        else:
            tasks[category].append(task_data)  # ✅ Store in regular tasks
            print(f"\n📌 BURDEN '{description}' ADDED TO '{category}' ({date}, {time}, {duration})")

        task_added = True  # ✅ Mark that at least one task was added

    # ✅ Only print "BURDEN LOCKED" if at least one task was successfully added
    if task_added:
        print("\n✅ BURDEN LOCKED.")

def view_burdens(tasks, daily_tasks):
    """Display tasks in a cleaner, more readable format, including properly categorized recurring tasks."""
    print("\nYOUR BURDENS:\n" + "=" * 40)

    # Merge daily (recurring) tasks into their original category
    categorized_recurring_tasks = {category: [] for category in tasks.keys()}

    for task in daily_tasks:
        category = task.get("category")
        if category and category in tasks:
            categorized_recurring_tasks[category].append(task)
        else:
            print(f"\n⚠️ RECURRING BURDEN '{task['description']}' HAS NO CATEGORY. DEFAULTING TO 'Not Urgent but Important'.")
            categorized_recurring_tasks["Not Urgent but Important"].append(task)

    # Display all tasks under their respective categories
    for category, task_list in tasks.items():
        total_tasks = len(task_list) + len(categorized_recurring_tasks[category])
        print(f"\n🔹 {category} ({total_tasks} BURDENS):")

        if total_tasks == 0:
            print("   (PITY, AN EMPTY VESSEL)\n")
            continue

        # Display regular tasks
        for i, task in enumerate(task_list, 1):
            description = task.get("description", "No description")
            start_time = task.get("start_time", "TBD")
            date = task.get("date", "Unknown")
            duration = task.get("duration", "Unknown")
            print(f"   {i}. {description} | ⏰ {start_time} | 📅 {date}")

        # Display recurring tasks in the same category
        for i, task in enumerate(categorized_recurring_tasks[category], len(task_list) + 1):
            description = task.get("description", "No description")
            start_time = task.get("start_time", "TBD") if "start_time" in task else "TBD"  # ✅ Fix: Ensure no KeyError
            date = task.get("date", "Unknown")  # ✅ Recurring tasks should have a default date
            print(f"   {i}. {description} | ⏰ {start_time} | 📅 {date} | (RECURRING)")

    print("=" * 40)

def shed_burdens(tasks, daily_tasks):
    """Remove a selected task from the list, including recurring burdens."""
    view_burdens(tasks, daily_tasks)  # ✅ Show current burdens before removal

    # ✅ Convert valid categories to lowercase for comparison
    valid_categories = {c.lower(): c for c in tasks.keys()}

    category_input = input("\nENTER THE CATEGORY OF THE BURDEN TO REMOVE.\n\nCATEGORY: ").strip()
    category = valid_categories.get(category_input.lower())

    if not category:
        print("\n⚠️ INVALID CATEGORY. REFRAME YOUR INTENT!")
        return

    # ✅ Gather tasks from both regular and recurring lists
    category_tasks = tasks[category]  # Regular tasks
    recurring_tasks = [task for task in daily_tasks if task["category"] == category]  # Recurring tasks in this category

    if not category_tasks and not recurring_tasks:
        print("\n⚠️ NO BURDENS IN THIS CATEGORY.")
        return

    # ✅ Display all tasks (regular & recurring)
    print(f"\n📌 BURDENS IN '{category}':")
    task_mapping = {}  # Map numbers to tasks
    index = 1

    for task in category_tasks:
        task_mapping[index] = ("Regular", category, task)
        print(f"{index}. {task['description']} | ⏰ {task['start_time']} | 📅 {task['date']}")
        index += 1

    for task in recurring_tasks:
        task_mapping[index] = ("Recurring", None, task)
        print(f"{index}. {task['description']} | ⏰ {task['start_time']} | 📅 {task['date']} (RECURRING)")
        index += 1

    # ✅ Ask for the task to remove
    try:
        task_num = int(input("\nENTER BURDEN NUMBER TO REMOVE: ").strip())
        if task_num in task_mapping:
            task_type, task_category, task = task_mapping[task_num]

            if task_type == "Regular":
                tasks[task_category].remove(task)
            else:
                daily_tasks.remove(task)

            print(f"\n✅ BURDEN '{task['description']}' LIFTED.")
        else:
            print("\n⚠️ INVALID NUMBER. REFRAME YOUR INTENT!")

    except ValueError:
        print("\n⚠️ INVALID INPUT. REFRAME YOUR INTENT!")

# ----- Helper Functions -----
def load_tasks(filename="tasks.json"):
    """Load tasks from a JSON file or initialize default structure."""
    try:
        with open(filename, "r") as file:
            data = json.load(file)
            return data.get("tasks", {}), data.get("daily_tasks", [])
    except (FileNotFoundError, json.JSONDecodeError):
        return {
            "Urgent & Important": [],
            "Not Urgent but Important": [],
            "Urgent but Not Important": [],
            "Not Urgent & Not Important": []
        }, []

def convert_to_24h(hour, minute, am_pm):
    """Convert 12-hour time to 24-hour format."""
    if am_pm.lower() == "pm" and hour != 12:
        hour += 12
    elif am_pm.lower() == "am" and hour == 12:
        hour = 0
    return hour, minute  # Returns in (hour, minute) format

def convert_duration_to_minutes(duration_str):
    """Convert duration like '2h 30m' into total minutes."""
    hours = 0
    minutes = 0
    parts = duration_str.split()
    for part in parts:
        if "h" in part:
            hours = int(part.replace("h", ""))
        elif "m" in part:
            minutes = int(part.replace("m", ""))
    return hours * 60 + minutes

def progress_report(tasks, daily_tasks):
    """Allows the user to update, postpone, or mark tasks as complete."""
    print("\nPROGRESS REPORT: REVIEW YOUR BURDENS.\n")

    # Show all tasks to pick from
    all_tasks = []
    task_mapping = {}

    index = 1
    for category, task_list in tasks.items():
        for task in task_list:
            task_mapping[index] = (category, task)
            print(f"{index}. {task['description']} | ⏰ {task['start_time']} | 📅 {task['date']} ({category})")
            index += 1

    for task in daily_tasks:
        task_mapping[index] = ("Recurring", task)

        # ✅ FIX: Ensure recurring task shows the actual time if set
        task_time = task.get("start_time", "TBD") if task.get("start_time") else "TBD"
        
        print(f"{index}. {task['description']} | ⏰ {task_time} (RECURRING)")
        index += 1

    if not task_mapping:
        print("⚠️ NO BURDENS TO UPDATE.")
        return

    # Ask which task to update
    try:
        choice = int(input("\nENTER THE NUMBER OF THE BURDEN TO UPDATE: ").strip())
        if choice not in task_mapping:
            print("⚠️ INVALID CHOICE.")
            return
    except ValueError:
        print("⚠️ INVALID INPUT.")
        return

    category, task = task_mapping[choice]

    # Ask what to do with the task
    print("\nWHAT SHALL BE DONE?")
    print("1. MARK AS COMPLETED ✅")
    print("2. POSTPONE 🔄")
    print("3. CANCEL ❌")

    action = input("\nSPEAK A NUMERAL: ").strip()

    if action == "1":
        # Remove completed task
        if category == "Recurring":
            daily_tasks.remove(task)
        else:
            tasks[category].remove(task)
        print(f"\n✅ BURDEN '{task['description']}' LIFTED.")

    elif action == "2":
        # Postpone task
        new_date = input("ENTER NEW DATE (YYYY-MM-DD): ").strip()
        try:
            datetime.strptime(new_date, "%Y-%m-%d")  # Validate date format
            task["date"] = new_date
            print(f"\n🔄 BURDEN '{task['description']}' MOVED TO {new_date}.")
        except ValueError:
            print("\n⚠️ INVALID DATE FORMAT. UPDATE FAILED.")

    elif action == "3":
        print("\n❌ UPDATE CANCELED.")

    else:
        print("\n⚠️ INVALID CHOICE.")

    # ✅ Save the updated tasks
    save_tasks(tasks, daily_tasks)

def save_tasks(tasks, daily_tasks, filename="tasks.json"):
    """Save tasks and daily tasks to a JSON file."""
    with open(filename, "w") as file:
        json.dump({"tasks": tasks, "daily_tasks": daily_tasks}, file, indent=4)

# ----- Main Program -----
def main():
    tasks, daily_tasks = load_tasks()
    while True:
        print("\nTHE INQUISITOR HAS DELIVERED YOU TO ME.")
        print("\nI AM VETRA, DAUGHTER OF THE INQUISITOR.")
        print("\nSTATE YOUR BURDENS, MORTAL.")
        print("\n1: ADD BURDEN.")
        print("2: VIEW BURDENS.")
        print("3: SHED BURDENS.")
        print("4: PROGRESS REPORT.")
        print("5: SAVE AND EXIT.")

        choice = input("\nSPEAK A NUMERAL: ").strip()

        if choice == "1":
            add_burdens(tasks, daily_tasks)
        elif choice == "2":
            view_burdens(tasks, daily_tasks)
        elif choice == "3":
            shed_burdens(tasks, daily_tasks)
        elif choice == "4":
            progress_report(tasks, daily_tasks)
        elif choice == "5":
            save_tasks(tasks, daily_tasks)
            print("\nBURDENS LOCKED, UNTIL WE MEET AGAIN, MORTAL.")
            break
        else:
            print("\nINVALID, REFRAME YOUR INTENT!")

if __name__ == "__main__":
    main()





