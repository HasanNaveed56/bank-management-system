class BankAccount:
    def __init__(self, name, acc_no, pin, balance=0):
        self.name = name
        self.acc_no = acc_no
        self.pin = pin
        self.balance = balance

    def check_balance(self):
        return self.balance

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            print(f"✔ {amount} deposited successfully.")
        else:
            print("❌ Invalid deposit amount. Please enter a positive value.")

    def withdraw(self, amount):
        if amount > self.balance:
            print("❌ Insufficient funds.")
        elif amount <= 0:
            print("❌ Invalid withdrawal amount. Please enter a positive value.")
        else:
            self.balance -= amount
            print(f"✔ {amount} withdrawn successfully.")

    def show_balance(self):
        print(f"💰 Current balance: {self.balance}")


# Example usage:
accounts = {}


def create_account():
    acc_no = input("Enter account number: ")
    if acc_no in accounts:
        print("❌ Account number already exists.")
        return
    name = input("Enter account holder's name: ")
    pin = input("Set a 4-digit PIN: ")

    accounts[acc_no] = BankAccount(name, acc_no, pin)
    print("✔ Account created successfully.")


def login():
    acc_no = input("Enter account number: ")
    pin = input("Enter PIN: ")
    account = accounts.get(acc_no)

    if account and account.pin == pin:
        print(f"✔ Welcome, {account.name}!")
        return account
    else:
        print("❌ Invalid account number or PIN.")
        return None


# main program
while True:
    print("\n1. Create Account\n2. Login\n3. Exit")
    choice = input("Choose an option: ")

    if choice == '1':
        create_account()
    elif choice == '2':
        user = login()
        if user:
            while True:
                print("\n1. Check Balance\n2. Deposit\n3. Withdraw\n4. Logout")
                action = input("Choose an action: ")

                if action == '1':
                    user.show_balance()
                elif action == '2':
                    try:
                        amount = float(input("Enter amount to deposit: "))
                    except ValueError:
                        print("❌ Enter a valid number.")
                        continue
                    user.deposit(amount)
                elif action == '3':
                    try:
                        amount = float(input("Enter amount to withdraw: "))
                    except ValueError:
                        print("❌ Enter a valid number.")
                        continue
                    user.withdraw(amount)
                elif action == '4':
                    print("✔ Logged out successfully.")
                    break
                else:
                    print("❌ Invalid option. Please try again.")
    elif choice == '3':
        print("✔ Exiting. Goodbye.")
        break
    else:
        print("❌ Invalid option. Please try again.")
