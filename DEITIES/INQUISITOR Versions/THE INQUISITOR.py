import random
import json
import os

# File to store user data
DATA_FILE = "hellforge_data.json"

# Load existing user data
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    return {}

# Save user data
def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

# Initialize user data
users = load_data()

# ----------------------------------------------------------------------------------------
# HELLFORGE - The Inquisitor with Tracking
# ----------------------------------------------------------------------------------------

# 🔥 Introduction: Identify the User
print("WELCOME TO HELL. I AM THE INQUISITOR. IDENTIFY YOURSELF, MORTAL.")
name = input("IDENTIFY YOURSELF, MORTAL: ").strip().lower()

# If new user, initialize their data
if name not in users:
    users[name] = {"days_trained": 0, "trials_completed": 0, "demons_faced": {}, "failures": 0}

# ----------------------------------------------------------------------------------------
# 🔥 Assessing the User's Purpose
print(f"SO, {name}, YOU DARE TO ENTER THE FORGE?")
print("DO YOU SEEK POWER, OR HAVE YOU STUMBLED HERE LIKE A LOST LAMB?")
answer = input().strip().lower()

power_responses = ["HAHAHA! GOOD. BUT POWER MUST BE EARNED.", "SEEKING POWER? PATHETIC. I WILL DECIDE IF YOU ARE WORTHY."]
weak_responses = ["THEN WHY ARE YOU HERE? TURN BACK NOW OR BE SHATTERED, MAGGOT!", "LOST LAMB? THEN PREPARE TO BE SLAUGHTERED."]

print(random.choice(power_responses) if "power" in answer else random.choice(weak_responses))

# ----------------------------------------------------------------------------------------
# 🔥 Tracking Training Progress
print("HOW MANY DAYS HAVE YOU TRAINED IN THE FORGE?")
try:
    days = int(input().strip())
    users[name]["days_trained"] += days
    if days == 0:
        print("YOU HAVE NOT EVEN BEGUN. LEAVE AND RETURN WHEN YOU ARE READY.")
    elif days < 7:
        print("PATHETIC. A WEEK IN HELL IS BUT A SINGLE BREATH.")
    elif 7 <= days < 30:
        print("YOU ENDURE, BUT YOU ARE FAR FROM FORGED.")
    else:
        print("YOU ARE NO LONGER A MORTAL. YOU BELONG TO THE FLAMES NOW.")
except ValueError:
    print("FOOL. NUMBERS ONLY. EVEN DEMONS CAN COUNT.")

# ----------------------------------------------------------------------------------------
# 🔥 The Inquisitor Tests Discipline
print("DID YOU CONSUME JUNK FOOD TODAY? (YES/NO)")
junk_food = input().strip().lower()

if junk_food == "yes":
    users[name]["failures"] += 1
    print("DISGUSTING. YOU HAVE FED THE DEMON OF INDULGENCE.")
    punishment = random.choice(["DROP AND GIVE ME 50!", "RUN UNTIL YOU REGRET IT!", "FAST FOR 12 HOURS. NO EXCEPTIONS."])
    print(punishment)
elif junk_food == "no":
    print("GOOD. GLUTTONY WILL NOT BE TOLERATED.")
else:
    print("DO NOT LIE TO ME, MORTAL.")

# ----------------------------------------------------------------------------------------
# 🔥 Facing the Demons
print("WHICH DEMON HAUNTS YOU? (FEAR, INDULGENCE, LAZINESS, DOUBT)")
demon = input().strip().lower()

if demon not in users[name]["demons_faced"]:
    users[name]["demons_faced"][demon] = 0
users[name]["demons_faced"][demon] += 1

demon_responses = {
    "fear": "FEAR IS AN ILLUSION. CONQUER IT OR IT WILL OWN YOU.",
    "indulgence": "YOU HAVE FED YOURSELF FOR TOO LONG. NOW YOU MUST STARVE.",
    "laziness": "EVERY SECOND YOU REST, A RIVAL GETS STRONGER.",
    "doubt": "THE WEAK DOUBT. THE STRONG KNOW. CHOOSE WHICH YOU ARE."
}
print(demon_responses.get(demon, "THAT DEMON IS UNKNOWN TO ME. BUT IT STILL MAKES YOU WEAK."))

# ----------------------------------------------------------------------------------------
# 🔥 Oath of the Hellforge
print("DO YOU SWEAR LOYALTY TO THE FORGE? (YES/NO)")
oath = input().strip().lower()

if oath == "yes":
    print("THEN YOU ARE MINE. THERE IS NO ESCAPE NOW.")
elif oath == "no":
    print("THEN WHY ARE YOU HERE? GO BACK TO YOUR SHELTER OF COMFORT.")
else:
    print("SPEAK CLEARLY OR BE DAMNED.")

# Save progress
save_data(users)








































