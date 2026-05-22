from flask import Flask, render_template, request, redirect, session
from model import Bank
from db import init_db

app = Flask(__name__)
app.secret_key = "secret123"

bank = Bank()


# ---------------- HOME ----------------
@app.route("/")
def home():
    return render_template("login.html")


# ---------------- LOGIN ----------------
@app.route("/login", methods=["POST"])
def login():
    user = bank.login_user(
        request.form["acc_no"],
        request.form["pin"]
    )

    if user:
        session["acc_no"] = user["acc_no"]
        return redirect("/dashboard")

    return "Invalid Login"


# ---------------- REGISTER ----------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        success = bank.create_user(
            request.form["name"],
            request.form["acc_no"],
            request.form["pin"]
        )

        if success:
            return redirect("/")

    return render_template("register.html")


# ---------------- DASHBOARD ----------------
@app.route("/dashboard")
def dashboard():
    if "acc_no" not in session:
        return redirect("/")

    return render_template(
        "dashboard.html",
        user=bank.get_user(session["acc_no"]),
        transactions=bank.get_transactions(session["acc_no"])
    )


# ---------------- DEPOSIT ----------------
@app.route("/deposit", methods=["POST"])
def deposit():
    if "acc_no" not in session:
        return redirect("/")

    bank.deposit(
        session["acc_no"],
        float(request.form["amount"])
    )

    return redirect("/dashboard")


# ---------------- WITHDRAW ----------------
@app.route("/withdraw", methods=["POST"])
def withdraw():
    if "acc_no" not in session:
        return redirect("/")

    bank.withdraw(
        session["acc_no"],
        float(request.form["amount"])
    )

    return redirect("/dashboard")


# ---------------- TRANSFER ----------------
@app.route("/transfer", methods=["POST"])
def transfer():
    if "acc_no" not in session:
        return redirect("/")

    bank.transfer(
        session["acc_no"],
        request.form["to_acc"],
        float(request.form["amount"])
    )

    return redirect("/dashboard")


# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# ---------------- START SERVER ----------------
if __name__ == "__main__":
    init_db()
    app.run(debug=True)