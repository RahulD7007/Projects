from connection import get_connection

def create_customer():
    con = get_connection()
    cur = con.cursor()

    fname = input("First Name: ")
    lname = input("Last Name: ")
    email = input("Email: ")

    cur.execute(
        "INSERT INTO customers (first_name, last_name, email) VALUES (:1, :2, :3)",
        (fname, lname, email)
    )

    con.commit()
    print("✅ Customer created")

    cur.close()
    con.close()


def create_account():
    con = get_connection()
    cur = con.cursor()

    cust_id = int(input("Customer ID: "))
    balance = float(input("Initial Balance: "))

    cur.execute(
        "INSERT INTO accounts (customer_id, balance) VALUES (:1, :2)",
        (cust_id, balance)
    )

    con.commit()
    print("✅ Account created")

    cur.close()
    con.close()


def deposit():
    con = get_connection()
    cur = con.cursor()

    acc_id = int(input("Account ID: "))
    amount = float(input("Amount: "))

    cur.execute(
        "UPDATE accounts SET balance = balance + :1 WHERE id = :2",
        (amount, acc_id)
    )

    cur.execute(
        "INSERT INTO transactions (account_id, txn_type, amount) VALUES (:1, 'DEPOSIT', :2)",
        (acc_id, amount)
    )

    con.commit()
    print("✅ Deposit successful")

    cur.close()
    con.close()


def withdraw():
    con = get_connection()
    cur = con.cursor()

    acc_id = int(input("Account ID: "))
    amount = float(input("Amount: "))

    cur.execute("SELECT balance FROM accounts WHERE id = :1", (acc_id,))
    result = cur.fetchone()

    if result and result[0] >= amount:
        cur.execute(
            "UPDATE accounts SET balance = balance - :1 WHERE id = :2",
            (amount, acc_id)
        )

        cur.execute(
            "INSERT INTO transactions (account_id, txn_type, amount) VALUES (:1, 'WITHDRAW', :2)",
            (acc_id, amount)
        )

        con.commit()
        print("✅ Withdrawal successful")
    else:
        print("❌ Insufficient balance")

    cur.close()
    con.close()


def view_accounts():
    con = get_connection()
    cur = con.cursor()

    cur.execute("SELECT * FROM accounts")

    for row in cur:
        print(row)

    cur.close()
    con.close()