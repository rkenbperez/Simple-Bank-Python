import random
import json
import bcrypt


def encrypt_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password


def verify_password(stored_password, provided_password):
    return bcrypt.checkpw(provided_password.encode('utf-8'), stored_password)


def register_user():
    name = input("Enter your name: ").strip().replace(" ", "").title()
    password = input("Enter your password: ").strip().replace(" ", "").title()

    balance = random.randint(1, 10000)

    try:
        with open('credentials.json', 'r') as file:
            users = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        users = {}

    if name in users:
        print("Username is already taken!")
        return

    hashed_password = encrypt_password(password)

    users[name] = {"password": hashed_password.decode('utf-8'), "balance": balance}

    with open('credentials.json', 'w') as file:
        json.dump(users, file)

    print(f"User {name} registered successfully! Your starting balance is ${balance}.")


def login_user():
    attempts = 0
    max_attempts = 3

    while attempts < max_attempts:
        name = input("Enter your name: ").strip().replace(" ", "").title()
        password = input("Enter your password: ")

        # Load the user data from the JSON file
        try:
            with open('credentials.json', 'r') as file:
                users = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            print("No users registered. Please register first.")
            return None, None

        # Validate the login credentials
        if name in users and verify_password(users[name]["password"].encode('utf-8'), password):
            print(f"Login successful! Welcome, {name}.")
            return name, users[name]["balance"]

        attempts += 1
        print(f"Invalid name or password. {max_attempts - attempts} attempts left.")
    
    print("Too many failed login attempts! Please try again.")
    return None, None

def withdraw(balance):
    try:
        withdraw_bal = int(input("How much would you like to withdraw:\n"))
        if withdraw_bal > balance:
            print("You don't have enough balance.")
        else:
            balance -= withdraw_bal
            print(f"You have withdrawn: ${withdraw_bal}")
            print(f"Your updated balance: ${balance}")
    except ValueError:
        print("Invalid input. Please enter a valid amount.")
    return balance

def deposit(balance):
    try:
        deposit_bal = int(input("How much would you like to deposit:\n"))
        balance += deposit_bal
        print(f"You have deposited: ${deposit_bal}")
        print(f"Your updated balance: ${balance}")
    except ValueError:
        print("Invalid input. Please enter a valid amount.")
    return balance

def view(balance):
    print(f"Your Balance: ${balance}")

def update_user_balance(name, balance):
    try:
        with open('credentials.json', 'r') as file:
            users = json.load(file)
        users[name]["balance"] = balance

        with open('credentials.json', 'w') as file:
            json.dump(users, file)
    except FileNotFoundError:
        print("Error updating balance. User data not found.")
    except json.JSONDecodeError:
        print("Error decoding JSON data.")


# Main program starts here
print("Welcome! Please register or log in.")

while True:
    action = input("Do you want to (1) Register or (2) Login? (3) Exit\n")

    if action == "1":
        register_user()
    elif action == "2":
        name, balance = login_user()
        if name is not None:  
            while True:
                print("Bank Menu:")
                choice = input("1. Withdraw 2. Deposit 3. View Balance 4. Logout\n")
               
                if choice == "1":
                    balance = withdraw(balance)
                    update_user_balance(name, balance)
                elif choice == "2":
                    balance = deposit(balance)
                    update_user_balance(name, balance)
                elif choice == "3":
                    view(balance)
                elif choice == "4":
                    print(f"Logging out, {name}.")
                    break
                else: 
                    print("Invalid choice. Please select 1, 2, 3, or 4.")
    elif action == "3":
        break       
    else:
        print("Invalid option. Please select either 1 or 2.")