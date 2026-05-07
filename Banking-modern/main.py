from functions import *

while True:
    print("\n==== BANK MENU ====")
    print("1. Create Customer")
    print("2. Create Account")
    print("3. Deposit")
    print("4. Withdraw")
    print("5. View Accounts")
    print("6. Exit")

    choice = input("Enter choice: ")

    if choice == "1":
        create_customer()
    elif choice == "2":
        create_account()
    elif choice == "3":
        deposit()
    elif choice == "4":
        withdraw()
    elif choice == "5":
        view_accounts()
    elif choice == "6":
        break
    else:
        print("Invalid choice")