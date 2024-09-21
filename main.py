
import tkinter as tk
from tkinter import messagebox
import sqlite3
import random

# Connect to database
conn = sqlite3.connect('skill_tracker.db')
cursor = conn.cursor()

# Global variables
user_id = None
skills_status = {}

# Function to switch between screens
def switch_to_skill_selection():
    # Hide the login frame
    login_frame.pack_forget()
    
    # Show the skill selection frame
    skill_selection_frame.pack(expand=True, fill="both")

# Function to create a new account
def sign_up():
    global user_id
    username = entry_username.get()
    email = entry_email.get()
    password = entry_password.get()

    if username and email and password:
        cursor.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)', (username, email, password))
        conn.commit()

        # Fetch the user_id of the newly created user
        cursor.execute('SELECT id FROM users WHERE username=? AND password=?', (username, password))
        user = cursor.fetchone()
        if user:
            user_id = user[0]

        messagebox.showinfo("Success", "Account created successfully!")
        switch_to_skill_selection()
    else:
        messagebox.showerror("Error", "Please fill in all fields.")

# Function to sign in
def sign_in():
    global user_id
    username = entry_username.get()
    password = entry_password.get()

    cursor.execute('SELECT id FROM users WHERE username=? AND password=?', (username, password))
    user = cursor.fetchone()

    if user:
        user_id = user[0]  # Store the user ID
        messagebox.showinfo("Success", "Logged in successfully!")
        switch_to_skill_selection()
    else:
        messagebox.showerror("Error", "Incorrect username or password.")

# Function to open the quiz based on selected skill
def open_quiz(skill):
    if skill == "Java":
        java_quiz()
    elif skill == "Python":
        python_quiz()
    elif skill == "JavaScript":
        javascript_quiz()
    else:
        messagebox.showerror("Error", "Quiz for this skill is not available.")

# Function to display the final status of all skills
def show_status():
    status_text = "Your Skills Status:\n\n"
    for skill, (level, rank) in skills_status.items():
        status_text += f"{skill} - Level: {level}, Rank: {rank}\n"
    
    lbl_status.config(text=status_text)
    quiz_frame.pack_forget()
    status_frame.pack(expand=True, fill="both")

# Function to finish a quiz and record the user's score
def finish_quiz(score, total_questions, skill_name):
    # Determine skill level and rank based on score
    if score == total_questions:
        level = 5
        rank = "Expert"
    elif score >= total_questions * 0.7:
        level = 3
        rank = "Intermediate"
    else:
        level = 1
        rank = "Beginner"

    # Update the skill status globally
    skills_status[skill_name] = (level, rank)

    # Store skill information in the database
    if user_id is not None:
        cursor.execute('INSERT INTO skills (user_id, skill_name, level, rank) VALUES (?, ?, ?, ?)',
                       (user_id, skill_name, level, rank))
        conn.commit()

    show_status()

# Common quiz logic
def quiz_logic(questions, skill_name):
    score = 0
    question_number = 0

    def ask_question():
        nonlocal score, question_number

        if question_number < len(questions):
            question, options, correct_answer = questions[question_number]
            lbl_question.config(text=question)
            random.shuffle(options)  # Shuffle options
            for i, option in enumerate(options):
                buttons[i].config(text=option, command=lambda option=option: check_answer(option, correct_answer))
        else:
            finish_quiz(score, len(questions), skill_name)

    def check_answer(selected_answer, correct_answer):
        nonlocal score, question_number
        if selected_answer == correct_answer:
            score += 1
        question_number += 1
        ask_question()

    # Create quiz layout
    lbl_question.pack(pady=10)
    for btn in buttons:
        btn.pack(fill="x", padx=20, pady=5)

    ask_question()

# Functions for each skill's quiz
def java_quiz():
    quiz_frame.pack(expand=True, fill="both")
    questions = [
        ("What is JVM?", ["Java Virtual Machine", "Java Volume Manager", "Java Version Manager", "Java Variable Machine"], "Java Virtual Machine"),
        ("Which keyword is used to define inheritance?", ["super", "this", "extend", "extends"], "extends"),
        ("Which is not a primitive data type?", ["int", "float", "String", "char"], "String"),
        ("Which class is the superclass of every class in Java?", ["Object", "String", "Main", "System"], "Object")
    ]
    quiz_logic(questions, "Java")

def python_quiz():
    quiz_frame.pack(expand=True, fill="both")
    questions = [
        ("What data type is the result of '3/2' in Python 3?", ["int", "float", "double", "long"], "float"),
        ("Which of the following is a mutable data type?", ["tuple", "list", "str", "int"], "list"),
        ("What is the output of 'print(2 ** 3)'?", ["6", "8", "9", "None"], "8"),
        ("Which keyword is used for function in Python?", ["def", "func", "lambda", "define"], "def")
    ]
    quiz_logic(questions, "Python")

def javascript_quiz():
    quiz_frame.pack(expand=True, fill="both")
    questions = [
        ("What is used to declare a variable in JavaScript?", ["var", "let", "const", "All of the above"], "All of the above"),
        ("Which company developed JavaScript?", ["Mozilla", "Netscape", "Microsoft", "Oracle"], "Netscape"),
        ("Which symbol is used for comments in JavaScript?", ["//", "#", "/* */", "--"], "//"),
        ("What is 'null' in JavaScript?", ["keyword", "literal", "datatype", "None of the above"], "literal")
    ]
    quiz_logic(questions, "JavaScript")

# UI Enhancements and Layouts
root = tk.Tk()
root.title("Skill Tracker")
root.geometry("360x640")
root.config(bg='#f0f8ff')

# Padding options for all elements
pad_options = {'padx': 10, 'pady': 10}

# Login frame
login_frame = tk.Frame(root, bg='#f0f8ff')
login_frame.pack(expand=True, fill="both")

label_username = tk.Label(login_frame, text="Username", font=("Arial", 14), bg='#f0f8ff')
label_username.pack(**pad_options)
entry_username = tk.Entry(login_frame, font=("Arial", 14))
entry_username.pack(**pad_options)

label_email = tk.Label(login_frame, text="Email (for Sign Up)", font=("Arial", 14), bg='#f0f8ff')
label_email.pack(**pad_options)
entry_email = tk.Entry(login_frame, font=("Arial", 14))
entry_email.pack(**pad_options)

label_password = tk.Label(login_frame, text="Password", font=("Arial", 14), bg='#f0f8ff')
label_password.pack(**pad_options)
entry_password = tk.Entry(login_frame, show="*", font=("Arial", 14))
entry_password.pack(**pad_options)

btn_sign_up = tk.Button(login_frame, text="Sign Up", command=sign_up, font=("Arial", 14), bg="lightgreen")
btn_sign_up.pack(**pad_options)

btn_sign_in = tk.Button(login_frame, text="Sign In", command=sign_in, font=("Arial", 14), bg="lightgreen")
btn_sign_in.pack(**pad_options)

# Skill selection frame
skill_selection_frame = tk.Frame(root, bg='#f0f8ff')

lbl_title = tk.Label(skill_selection_frame, text="Select a Skill to Take the Quiz", font=("Arial", 16), bg='#f0f8ff')
lbl_title.pack(pady=20)

skills = ["Java", "Python", "JavaScript"]
for skill in skills:
    tk.Button(skill_selection_frame, text=skill, font=("Arial", 14), command=lambda skill=skill: open_quiz(skill)).pack(pady=10)

# Quiz frame
quiz_frame = tk.Frame(root, bg='#f0f8ff')
lbl_question = tk.Label(quiz_frame, text="", font=("Arial", 14), bg='#f0f8ff')
buttons = [tk.Button(quiz_frame, text="", font=("Arial", 12)) for _ in range(4)]

# Status frame
status_frame = tk.Frame(root, bg='#f0f8ff')
lbl_status = tk.Label(status_frame, text="", font=("Arial", 14), bg='#f0f8ff')
lbl_status.pack(pady=20)
btn_close = tk.Button(status_frame, text="Close", command=root.quit, font=("Arial", 14))
btn_close.pack(pady=10)

# Start the main loop
root.mainloop()
