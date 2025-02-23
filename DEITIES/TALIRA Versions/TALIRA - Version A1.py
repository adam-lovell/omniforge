import json
import re
from datetime import datetime
import smtplib
from email.message import EmailMessage

TALIRA_GREETING = "THE INQUISITOR HAS SENT YOU TO ME. I AM TALIRA, DEITY OF COIN. WHAT IS IT YOU WISH TO DO?"
MENU_OPTIONS = [
    "1. ADD OR UPDATE MONTHLY INCOME",
    "2. ADD EXPENSE MANUALLY",
    "3. VIEW SUMMARY OF EXPENSES",
    "4. SET UP PAYMENT REMINDERS WITH EMAIL NOTIFICATIONS",
    "5. SAVE AND EXIT"
]

data_file = "talira_data.json"

def load_data():
    try:
        with open(data_file, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"income": 0, "transactions": [], "subscriptions": {}}

def save_data(data):
    with open(data_file, "w") as f:
        json.dump(data, f, indent=4)

def set_income(data):
    print("LOOK AT YOUR BANK STATEMENT. HOW MUCH DO YOU MAKE AFTER TAXES?")
    income = float(input("ENTER YOUR MONTHLY INCOME: "))
    data["income"] = income
    print(f"INCOME SET TO ${income:.2f}")
    save_data(data)

def add_expense(data):
    print("ENTER YOUR EXPENSE DETAILS.")
    date = input("DATE (MM/DD/YYYY): ")
    desc = input("DESCRIPTION: ")
    amount = float(input("AMOUNT (USE NEGATIVE FOR EXPENSES): "))
    data["transactions"].append({"date": date, "description": desc.strip(), "amount": amount})
    print("EXPENSE ADDED.")
    save_data(data)

def view_summary(data):
    income = data["income"]
    expenses = sum(txn["amount"] for txn in data["transactions"] if txn["amount"] < 0)
    balance = income + expenses
    print(f"MONTHLY INCOME: ${income:.2f}")
    print(f"TOTAL EXPENSES: ${abs(expenses):.2f}")
    print(f"ESTIMATED REMAINING BALANCE: ${balance:.2f}")

def send_email_reminder(email, name, amount, due_date):
    msg = EmailMessage()
    msg.set_content(f"REMINDER: {name} payment of ${amount:.2f} is due on {due_date}.")
    msg["Subject"] = f"Payment Reminder: {name} Due on {due_date}"
    msg["From"] = "talira@hellforge.com"
    msg["To"] = email

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login("your-email@gmail.com", "your-email-password")
            server.send_message(msg)
        print(f"EMAIL REMINDER SENT TO {email} FOR {name} DUE ON {due_date}.")
    except Exception as e:
        print(f"FAILED TO SEND EMAIL: {e}")

def setup_reminders(data):
    print("ENTER RECURRING PAYMENTS (E.G., NETFLIX, RENT, GYM MEMBERSHIP). TYPE 'DONE' TO FINISH.")
    email = input("ENTER YOUR EMAIL TO RECEIVE REMINDERS: ")
    while True:
        name = input("SUBSCRIPTION NAME: ")
        if name.lower() == "done":
            break
        amount = float(input(f"HOW MUCH DO YOU PAY FOR {name}? $"))
        date_due = input("WHEN IS IT DUE EACH MONTH? (FORMAT: MM/DD)")
        data["subscriptions"][name] = {"amount": amount, "due_date": date_due, "email": email}
        send_email_reminder(email, name, amount, date_due)
        print(f"REMINDER SET FOR {name}: ${amount} DUE ON {date_due}")
    save_data(data)

def main():
    data = load_data()
    print(TALIRA_GREETING)
    while True:
        print("\n" + "\n".join(MENU_OPTIONS))
        choice = input("CHOOSE AN OPTION: ")
        if choice == "1":
            set_income(data)
        elif choice == "2":
            add_expense(data)
        elif choice == "3":
            view_summary(data)
        elif choice == "4":
            setup_reminders(data)
        elif choice == "5":
            print("EXITING TALIRA. RETURNING TO THE INQUISITOR...")
            break
        else:
            print("INVALID OPTION. TRY AGAIN.")

if __name__ == "__main__":
    main()

