# Personalized Task Manager

A lightweight, customizable task management application built using Python and Flask with an HTML/CSS/JavaScript frontend. Designed to help users effectively organize tasks, track progress, and stay productive while maintaining data privacy through local storage.

## Objective

To develop a personalized, user-friendly task management tool that operates offline, allows full CRUD operations on tasks, and supports deadlines, prioritization, and progress tracking.

## Features

- Add, view, update, and delete tasks
- Mark tasks as pending, in-progress, or completed
- Categorize tasks and assign priority levels
- Set and track deadlines
- Store task data locally using SQLite or JSON
- User authentication with secure session management
- Command-Line and Web UI interface
- Designed for privacy and offline use

## Technologies Used

- **Backend:** Python 3.x, Flask, Flask-SQLAlchemy
- **Frontend:** HTML, CSS, JavaScript
- **Database:** SQLite or JSON
- **Notifications (optional):** Twilio API for SMS alerts

## Project Structure
project/
├── app.py 
├── models.py 
├── templates/
│ ├── index.html
│ └── dashboard.html
├── static/ 
│ ├── style.css
│ └── script.js
├── tasks.db
├── requirements.txt
└── README.md 

