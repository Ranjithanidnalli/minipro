
from flask import Flask, render_template, redirect, request, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from twilio.rest import Client
import os

app = Flask(__name__)
app.secret_key = "your_secret_key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Twilio Configuration
TWILIO_ACCOUNT_SID = 'your_account_sid'
TWILIO_AUTH_TOKEN = 'your_auth_token'
TWILIO_PHONE_NUMBER = '+1234567890'
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(15), nullable=False)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    task_name = db.Column(db.String(100), nullable=False)
    deadline = db.Column(db.String(50), nullable=False)
    priority = db.Column(db.String(10), nullable=False)

# Routes
@app.route("/")
def home():
    if "user_id" in session:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        full_name = request.form["full_name"]
        email = request.form["email"]
        phone = request.form["phone"]

        new_user = User(username=username, password=password, full_name=full_name, email=email, phone=phone)
        db.session.add(new_user)
        db.session.commit()
        flash("Registration successful! Please log in.")
        return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username, password=password).first()
        if user:
            session["user_id"] = user.id
            session["username"] = user.username
            flash("Login successful!")
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid credentials.")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully.")
    return redirect(url_for("login"))

from datetime import datetime, timedelta

@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))

    user_id = session["user_id"]
    tasks = Task.query.filter_by(user_id=user_id).all()

    now = datetime.now()
    notifications = []

    for task in tasks:
        deadline_datetime = datetime.strptime(task.deadline, "%Y-%m-%d %H:%M")

        time_left = deadline_datetime - now
        if time_left < timedelta(hours=0):
            notifications.append(f"Task '{task.task_name}' is overdue!")
        elif time_left < timedelta(hours=24):
            notifications.append(f"Task '{task.task_name}' is due soon! Only {time_left} left.")

    if request.method == "POST":
        task_name = request.form["task"]
        deadline_date = request.form["deadline_date"]
        deadline_time = request.form["deadline_time"]
        priority = request.form["priority"]
        deadline = f"{deadline_date} {deadline_time}"

        new_task = Task(user_id=user_id, task_name=task_name, deadline=deadline, priority=priority)
        db.session.add(new_task)
        db.session.commit()
        flash("Task added successfully!")
        return redirect(url_for("dashboard"))

    return render_template("dashboard.html", tasks=tasks, notifications=notifications)


@app.route("/delete_task/<int:task_id>")
def delete_task(task_id):
    task = Task.query.get(task_id)
    db.session.delete(task)
    db.session.commit()
    flash("Task deleted successfully!")
    return redirect(url_for("dashboard"))

@app.route("/send_sms/<int:task_id>")
def send_sms(task_id):
    task = Task.query.get(task_id)
    user = User.query.get(task.user_id)

    message_body = f"Reminder: Your task '{task.task_name}' is due on {task.deadline}."
    client.messages.create(to=user.phone, from_=TWILIO_PHONE_NUMBER, body=message_body)
    flash("SMS sent successfully!")
    return redirect(url_for("dashboard"))

if __name__ == "__main__":
    with app.app_context():  # Wrap in app context
        db.create_all()  # Create the database tables (if not already created)
    app.run(debug=True)

