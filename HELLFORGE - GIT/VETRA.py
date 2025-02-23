import json
from datetime import datetime
from datetime import datetime, timedelta  # ✅ Ensure timedelta is imported

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

def save_tasks(tasks, daily_tasks, filename="tasks.json"):
    """Save tasks and daily tasks to a JSON file."""
    with open(filename, "w") as file:
        json.dump({"tasks": tasks, "daily_tasks": daily_tasks}, file, indent=4)

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

# ----- Core Task Functions -----
def add_task_bulk(tasks):
    """Prompt user to add multiple tasks in one input."""
    print("\nBULK TASK ENTRY:")
    print("\nCATEGORIES: Urgent & Important, Not Urgent but Important, Urgent but Not Important, Not Urgent & Not Important")
    print("\nFORMAT AS: DESCRIPTION, CATEGORY, DATE (YYYY-MM-DD), TIME (HH:MM AM/PM), DURATION (e.g., 2h 30m))")
    print("\nSEPARATE YOUR BURDENS WITH ';'")
    
    user_input = input("\nENTER BURDENS: ").strip()
    task_entries = user_input.split(";")
    
    valid_categories = {c.lower(): c for c in tasks.keys()}  # Allow case-insensitive matching
    task_added = False  # 🔥 Flag to track if any task was successfully added

    # ✅ Ask if the task is recurring
        # ✅ Ensure description is properly defined before asking if it's recurring
    task_data = {
        "description": description,
        "date": date,
        "start_time": time,
        "duration": duration
    }

    is_recurring = input(f"\nIS '{task_data['description']}' A RECURRING DAILY BURDEN? (YES/NO): ").strip().lower() == "yes"


    task_data = {
        "description": description,
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

    for entry in task_entries:
        parts = [p.strip() for p in entry.split(",")]
        
        if len(parts) != 5:
            print(f"\nINVALID FORMAT FOR: {entry}")
            print("\nREFRAME YOUR INTENT MORTAL!")
            continue

        description, category, date, time, duration = parts
        category = valid_categories.get(category.lower())
        
        if not category:
            print(f"\nINVALID CATEGORY ENTRY FOR: {category}")
            print("\nREFRAME YOUR INTENT MORTAL!")
            continue

        # Validate date format
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            print(f"\nINVALID DATE FORMAT FOR: {date}")
            print("\nREFRAME YOUR INTENT MORTAL!")
            continue
        
        # Validate time format
        try:
            datetime.strptime(time, "%I:%M %p")
        except ValueError:
            print(f"\nINVALID DATE FORMAT FOR: {time}")
            print("\nREFRAME YOUR INTENT MORTAL!")
            continue

        # Validate duration format
        if not any(char.isdigit() for char in duration):
            print(f"\nINVALID DURATION FORMAT FOR: {duration}")
            print("\nREFRAME YOUR INTENT MORTAL!")
            continue

        # ✅ Convert time to 24-hour format for sorting
        time_parts = time.split(" ")
        hour, minute = map(int, time_parts[0].split(":"))
        am_pm = time_parts[1]
        start_hour, start_minute = convert_to_24h(hour, minute, am_pm)
        start_time_24h = start_hour * 60 + start_minute  # Convert to minutes for comparison

        # Convert duration to total minutes
        duration_minutes = convert_duration_to_minutes(duration)

        # Check for overlapping tasks
        conflict = False
        for task in tasks[category]:
            existing_time_parts = task['start_time'].split(" ")
            existing_hour, existing_minute = map(int, existing_time_parts[0].split(":"))
            existing_am_pm = existing_time_parts[1]
            existing_start_hour, existing_start_minute = convert_to_24h(existing_hour, existing_minute, existing_am_pm)
            existing_start_time = existing_start_hour * 60 + existing_start_minute
            existing_duration = convert_duration_to_minutes(task['duration'])
            existing_end_time = existing_start_time + existing_duration

            new_end_time = start_time_24h + duration_minutes

            if start_time_24h < existing_end_time and new_end_time > existing_start_time:
                print(f"OVERLAPPING BURDENS: '{description}' conflicts with '{task['description']}' ({task['start_time']})")
                conflict = True
                break
            
        # ✅ Allow user to override the conflict warning
        if conflict:
            override = input("WILL YOU ADD THIS BURDEN REGARDLESS? (YES/NO): ").strip().lower()
            if override != "yes":
                print(f"BURDEN '{description}' NOT ADDED DUE TO CONFLICT.")
                continue

        # ✅ Ask if the task is for tomorrow
        next_day = input(f"\nIS '{description}' FOR TOMORROW? (YES/NO): ").strip().lower() == "yes"

        # Score the task              
        tasks[category].append({
            "description": description,
            "date": date,
            "start_time": time,
            "duration": duration
        })
        
        print(f"\nBURDEN '{description}' ADDED TO '{category}' ({date}, {time}, {duration})")
        task_added = True  # ✅ Mark that at least one task was added

    # ✅ Only print "BURDEN LOCKED" if at least one task was successfully added
    if task_added:
        print("\nBURDEN LOCKED.")

def view_tasks(tasks):
    """Display tasks in a cleaner, more readable format."""
    print("\nYOUR BURDENS:\n" + "=" * 40)
    
    for category, task_list in tasks.items():
        print(f"\n🔹 {category} ({len(task_list)} BURDENS):")
        if not task_list:
            print("   (PITY, AN EMPTY VESSEL)\n")
            continue
        
        for i, task in enumerate(task_list, 1):
            description = task.get("description", "No description")
            start_time = task.get("start_time", "TBD")
            duration = task.get("duration", "Unknown")
            print(f"   {i}. {description}")
            print(f"   📅 Date: {task['date']} | ⏳ Duration: {task['duration']} | ⏰ Start: {task['start_time']}")


    print("=" * 40)

def view_next_day_plan(tasks, daily_tasks):
    """Display tasks scheduled for the next day, including daily tasks."""
    print("\nTOMORROW'S BATTLE PLAN.")
    print("=" * 40)

    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    next_day_tasks = []

    # ✅ Collect scheduled tasks for tomorrow
    for category, task_list in tasks.items():
        for task in task_list:
            if task["date"] == tomorrow:  # ✅ Ensure it checks tomorrow's date
                next_day_tasks.append(f"📝 {task['description']} at {task['start_time']} ({task['duration']}) - {category}")

    # ✅ Include recurring daily tasks (which apply every day)
    for daily_task in daily_tasks:
        next_day_tasks.append(f"🔄 {daily_task['description']} at {daily_task['time']} (Daily)")

    # ✅ Display tasks or indicate none
    if next_day_tasks:
        for task in sorted(next_day_tasks):
            print(task)
    else:
        print("\n⚠️ NO BURDENS AWAIT YOU TOMORROW, MORTAL. EVERY GENERAL MUST PLAN.")

def remove_task(tasks):
    """Remove a selected task."""
    view_tasks(tasks)
    category = input("\nENTER CATEGORY: ").strip()
    
    if category not in tasks:
        print("\nINVALID, REFRAME YOUR INTENT!")
        return
    
    for i, task in enumerate(tasks[category], 1):
        print(f"{i}: {task['description']}")
    task_num = input("\nENTER BURDEN NUMERAL: ").strip()
    
    if task_num.isdigit() and 1 <= int(task_num) <= len(tasks[category]):
        removed = tasks[category].pop(int(task_num) - 1)
        print(f"BURDEN LIFTED: {removed['description']}")
    else:
        print("\nINVALID, REFRAME YOUR INTENT!")

def generate_daily_plan(tasks, daily_tasks):
    """Generate and display a structured daily plan with AM/PM and break options."""
    print("\nRECURRING BURDENS:")

    if daily_tasks or any(task_list for task_list in tasks.values() if task_list):  
        print("\nBEFORE EMBARKING, SET A TIMER, SILENCE YOUR DEVICES, AND SETTLE YOUR MIND WITH MELODIES (LOFI, JAZZ, CLASSICAL MUSIC).")
    else:
        print("\nNO BURDENS DETECTED. GO FORTH OR ADD A BURDEN.")
        return  # Exit if no burdens exist

    # ✅ Ensure there are actual tasks before proceeding
    total_tasks = sum(len(task_list) for task_list in tasks.values())
    if total_tasks == 0:
        print("\nNO BURDENS DETECTED. DO NOT TEST MY PATIENCE, MORTAL!")
        return

    # ✅ Get the starting time **once** instead of per task
    while True:
        try:
            start_hour = int(input("\nENTER START HOUR (1-12): "))
            start_minute = int(input("ENTER START MINUTES (0-59): "))
            am_pm = input("AM or PM?: ").strip().upper()
            if am_pm not in ["AM", "PM"]:
                raise ValueError("INVALID TIME INPUT, SPEAK WITH CLARITY!")
            break
        except ValueError:
            print("INVALID TIME INPUT, SPEAK WITH CLARITY!")

    # ✅ Convert start time to 24-hour format
    current_hour, current_minute = convert_to_24h(start_hour, start_minute, am_pm)  
    current_time = (current_hour * 60) + current_minute  # Convert to total minutes

    print("\nYOUR DAILY BURDEN PLAN:")
    print("=" * 40)

    task_found = False  # Track if at least one task is processed

    for category, task_list in tasks.items():
        if not task_list:
            continue  # Skip empty categories

        print(f"\n{category} ({len(task_list)} tasks)")
        task_found = True

        for task in task_list:
            duration_minutes = convert_duration_to_minutes(task["duration"])

            # ✅ Format time properly
            display_hour = (current_time // 60) % 12 or 12
            display_minute = current_time % 60
            display_am_pm = "AM" if current_time < 720 else "PM"
            formatted_time = f"{display_hour}:{display_minute:02} {display_am_pm}"

            print(f"\n⏳ {formatted_time} | 📝 {task['description']} ({task['duration']})")

            # ✅ Move current time forward
            current_time += duration_minutes

            # ✅ Ask if user wants a break
            if input("\nWILL YOU ADD A BREAK? (YES/NO): ").strip().lower() == "yes":
                while True:
                    try:
                        break_time = int(input("ENTER BREAK DURATION (minutes): "))
                        break
                    except ValueError:
                        print("\nINVALID, REFRAME YOUR INTENT!")

                current_time += break_time
                print(f"\n🛑 BREAK: {break_time} minutes")
                
            if task_found:
                print("\n✅ PLAN OF ATTACK CREATED.")
            print("\nMARK THESE TASKS IN YOUR MOST TRUSTED CALENDAR/REMINDERS APP AND GET STARTED:")

            for category, task_list in tasks.items():
                for task in task_list:
                    print("\n==============================")
                    print(f"📌 TASK: {task['description']}")  # ✅ Task Name
                    print(f"📅 CATEGORY: {category}")  # ✅ Task Category
                    print(f"⏰ START TIME: {formatted_time}")  # ✅ FIXED: Uses formatted_time
                    print(f"⌛ DURATION: {task['duration']}")  # ✅ Task Duration
                    if 'break_time' in task and task['break_time']:  # ✅ Ensures breaks print properly
                        print(f"🛑 BREAK: {task['break_time']} minutes")
            print("\n==============================")

        else:
            print("\n⚠️ FIRST, SPEAK TO ME A BURDEN YOU CARRY.")

def end_of_day_log(tasks):
    """Log completed tasks and remove them if completed."""
    for category, task_list in tasks.items():
        for task in task_list[:]:
            completed = input(f"\nDID YOU COMPLETE '{task['description']}'? (YES/NO): ").strip().lower()
            if completed == "yes":
                task_list.remove(task)
    print("\nPROGRESS LOGGED, CONTINUE FORTH AND DO NOT FALTER.")

def plan_for_next_day(tasks):
    """Roll over unfinished tasks to the next day's schedule and adjust durations if needed."""
    
    next_day = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")  # ✅ Get tomorrow's date

    for category, task_list in tasks.items():
        for task in task_list:
            completed = input(f"\nDID YOU COMPLETE '{task['description']}' ? (YES/NO): ").strip().lower()
            
            if completed == "no":
                extra_time = input("\nENTER ADDITIONAL TIME NEEDED (e.g., 1h 30m): ").strip()
                task['duration'] = extra_time  
                task['date'] = next_day  # ✅ Move task to tomorrow
                
                print(f"\n🔄 '{task['description']}' MOVED TO TOMORROW WITH NEW DURATION: {task['duration']}")

    save_tasks(tasks, daily_tasks)  # ✅ Ensure tasks persist
    print("\n✅ TOMORROW'S BURDENS LOCKED. WELL DONE, MORTAL.")

def add_daily_task(tasks, daily_tasks):
    """Function to add recurring daily tasks and save them immediately."""

    task_desc = input("\nDESCRIBE YOUR DAILY BURDEN: ").strip()
    if not task_desc:
        print("INVALID, REFRAME YOUR INTENT!")
        return

    task_time = input("\nENTER HOUR OF EXECUTION FOR YOUR BURDEN (HH:MM AM/PM): ").strip()

    # ✅ Ensure proper time format
    try:
        datetime.strptime(task_time, "%I:%M %p")  # Validate format
    except ValueError:
        print("INVALID FORMAT, SPEAK WITH CLARITY! FORMAT AS, HH:MM AM/PM.")
        return

    # ✅ Store the daily task
    task_info = {"description": task_desc, "time": task_time}
    daily_tasks.append(task_info)

    # ✅ Automatically save tasks
    save_tasks(tasks, daily_tasks)

    print(f"\nRECURRING BURDEN '{task_desc}' LOCKED IN FOR {task_time}, DAILY. ETCH THIS INTO YOUR BINDING LEDGER.")

def remove_daily_task(daily_tasks):
    """Remove a recurring burden."""
    if not daily_tasks:
        print("\nNO RECURRING BURDENS TO REMOVE.")
        return
    
    print("\nYOUR RECURRING BURDENS:")
    for i, task in enumerate(daily_tasks, 1):
        print(f"{i}: {task['description']} at {task['time']}")

    try:
        choice = int(input("\nENTER NUMBER TO REMOVE: ")) - 1
        if 0 <= choice < len(daily_tasks):
            removed = daily_tasks.pop(choice)
            print(f"\nBURDEN '{removed['description']}' REMOVED.")
        else:
            print("\nINVALID CHOICE. REFRAME YOUR INTENT!")
    except ValueError:
        print("\nINVALID INPUT. SPEAK WITH CLARITY!")

def view_next_day_plan(tasks, daily_tasks):
    """Display the tasks scheduled for the next day."""
    print("\nTOMORROW'S BATTLE PLAN.\n")
    print("===================================")

    next_day = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    tasks_tomorrow = [
        task for category in tasks.values() for task in category if task["date"] == next_day
    ]

    if daily_tasks:
        print("\nRECURRING BURDENS:")
        for task in daily_tasks:
            print(f"\n  - {task['description']} at {task['time']}")

    if not tasks_tomorrow and not daily_tasks:
        print("\nNO BURDENS AWAIT YOU TOMORROW, MORTAL. EVERY GENERAL MUST PLAN.")

    else:
        print("\nTHESE BURDENS AWAIT YOU. YOU MUST FOCUS, PLAN, AND EXECUTE.")
        for task in tasks_tomorrow:
            print(f"  - {task['description']} at {task['start_time']} ({task['duration']})")

    print("\n===================================")

# ----- Main Program -----
def main():
    tasks, daily_tasks = load_tasks()
    while True:
        print("\nTHE INQUISITOR HAS DELIVERED YOU TO ME.")
        print("\nI AM VETRA, DAUGHTER OF THE INQUISITOR.")
        print("\nSTATE YOUR BURDENS, MORTAL.")
        print("\n1: ADD BURDEN.")
        print("2: VIEW BURDENS.")
        print("3: SHED BURDEN.")
        print("4: GENERATE A PLAN.")
        print("5: PROGRESS REPORT.")
        print("6: PLAN FOR TOMORROW.")
        print("7: REMOVE RECURRING BURDEN.")
        print("8: SEE TOMORROW'S BATTLE.")
        print("9: SAVE AND EXIT.")

        choice = input("\nSPEAK A NUMERAL: ").strip()

        if choice == "1":
            add_task_bulk(tasks)
        elif choice == "2":
            view_tasks(tasks)
        elif choice == "3":
            remove_task(tasks)
        elif choice == "4":
            generate_daily_plan(tasks, daily_tasks)
        elif choice == "5":
            end_of_day_log(tasks)
        elif choice == "6":
            plan_for_next_day(tasks)
        elif choice == "7":
            remove_daily_task(daily_tasks)
        elif choice == "8":
            view_next_day_plan(tasks, daily_tasks)
        elif choice == "9":
            save_tasks(tasks, daily_tasks)
            print("\nBURDENS LOCKED, UNTIL WE MEET AGAIN, MORTAL.")
            break
        else:
            print("\nINVALID, REFRAME YOUR INTENT!")

if __name__ == "__main__":
    main()
