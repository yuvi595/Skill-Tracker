import sqlite3




# Connect to the SQLite database (it will create a new one if it doesn't exist)
conn = sqlite3.connect('skill_tracker.db')




# Create a cursor object to execute SQL commands
cursor = conn.cursor()




# Create a table for users
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    email TEXT NOT NULL,
                    password TEXT NOT NULL
                )''')




# Create a table for skills
cursor.execute('''CREATE TABLE IF NOT EXISTS skills (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    skill_name TEXT NOT NULL,
                    level INTEGER DEFAULT 1,
                    rank TEXT,
                    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
                )''')




# Create a table for quizzes
cursor.execute('''CREATE TABLE IF NOT EXISTS quizzes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    skill_id INTEGER,
                    question TEXT,
                    correct_answer TEXT,
                    FOREIGN KEY(skill_id) REFERENCES skills(id) ON DELETE CASCADE
                )''')




# Commit changes and close connection
conn.commit()
conn.close()




print("Database setup complete.")