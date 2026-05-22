from db import get_connection
from werkzeug.security import generate_password_hash, check_password_hash

class Bank:

    # CREATE ACCOUNT
    def create_user(self, name, acc_no, pin):
        conn = get_connection()
        cur = conn.cursor()

        hashed_pin = generate_password_hash(pin)

        try:
            cur.execute("""
                INSERT INTO users (name, acc_no, pin, balance)
                VALUES (?, ?, ?, 0)
            """, (name, acc_no, hashed_pin))

            conn.commit()
            return True

        except Exception as e:
            print(e)
            return False

        finally:
            conn.close()

    # LOGIN
    def login_user(self, acc_no, pin):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("SELECT * FROM users WHERE acc_no=?", (acc_no,))
        user = cur.fetchone()

        conn.close()

        if user and check_password_hash(user["pin"], pin):
            return user

        return None

    # GET USER
    def get_user(self, acc_no):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("SELECT * FROM users WHERE acc_no=?", (acc_no,))
        user = cur.fetchone()

        conn.close()
        return user

    # DEPOSIT
    def deposit(self, acc_no, amount):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            "UPDATE users SET balance = balance + ? WHERE acc_no=?",
            (amount, acc_no)
        )

        cur.execute(
            "INSERT INTO transactions (acc_no, type, amount) VALUES (?, 'DEPOSIT', ?)",
            (acc_no, amount)
        )

        conn.commit()
        conn.close()

    # WITHDRAW
    def withdraw(self, acc_no, amount):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("SELECT balance FROM users WHERE acc_no=?", (acc_no,))
        user = cur.fetchone()

        if not user or user["balance"] < amount:
            conn.close()
            return False

        cur.execute(
            "UPDATE users SET balance = balance - ? WHERE acc_no=?",
            (amount, acc_no)
        )

        cur.execute(
            "INSERT INTO transactions (acc_no, type, amount) VALUES (?, 'WITHDRAW', ?)",
            (acc_no, amount)
        )

        conn.commit()
        conn.close()
        return True

    # TRANSFER
    def transfer(self, from_acc, to_acc, amount):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("SELECT balance FROM users WHERE acc_no=?", (from_acc,))
        sender = cur.fetchone()

        if not sender:
            conn.close()
            return "Sender not found"

        if sender["balance"] < amount:
            conn.close()
            return "Insufficient balance"

        cur.execute("SELECT * FROM users WHERE acc_no=?", (to_acc,))
        receiver = cur.fetchone()

        if not receiver:
            conn.close()
            return "Receiver not found"

        cur.execute(
            "UPDATE users SET balance = balance - ? WHERE acc_no=?",
            (amount, from_acc)
        )

        cur.execute(
            "UPDATE users SET balance = balance + ? WHERE acc_no=?",
            (amount, to_acc)
        )

        cur.execute(
            "INSERT INTO transactions (acc_no, type, amount) VALUES (?, 'TRANSFER OUT', ?)",
            (from_acc, amount)
        )

        cur.execute(
            "INSERT INTO transactions (acc_no, type, amount) VALUES (?, 'TRANSFER IN', ?)",
            (to_acc, amount)
        )

        conn.commit()
        conn.close()

        return "SUCCESS"

    # TRANSACTIONS
    def get_transactions(self, acc_no):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            "SELECT * FROM transactions WHERE acc_no=? ORDER BY id DESC",
            (acc_no,)
        )

        data = cur.fetchall()
        conn.close()
        return data