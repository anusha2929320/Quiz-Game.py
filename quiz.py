import tkinter as tk
from tkinter import messagebox

# List of questions with options and correct answers
questions = [
    {
        "question": "Which planet is known as the Red Planet?",
        "options": ["Earth", "Mars", "Jupiter", "Venus"],
        "answer": "Mars"
    },
    {
        "question": "Who invented the telephone?",
        "options": ["Alexander Graham Bell", "Thomas Edison", "James Watt", "Isaac Newton"],
        "answer": "Alexander Graham Bell"
    },
    {
        "question": "Who was the first man to step on the moon?",
        "options": ["Yuri Gagarin", "Neil Armstrong", "Buzz Aldrin", "Rakesh Sharma"],
        "answer": "Neil Armstrong"
    },
    {
        "question": "Which element has the chemical symbol 'O'?",
        "options": ["Oxygen", "Oxide", "Orpiment", "Osmium"],
        "answer": "Oxygen"
    },
    {
        "question": "Which country is called the Land of the Rising Sun?",
        "options": ["India", "Japan", "Australia", "China"],
        "answer": "Japan"
    },
    {
        "question": "Which city is known as the 'City of Joy' in India?",
        "options": ["Mumbai", "Chennai", "Kolkata", "Hyderabad"],
        "answer": "Kolkata"
    },
    {
        "question": "How many players are there in a cricket team (on the field during play)?",
        "options": ["9", "11", "8", "7"],
        "answer": "11"
    },
    {
        "question": "Which is the smallest bone in the human body?",
        "options": ["Stapes", "Femur", "Ulna", "Radius"],
        "answer": "Stapes"
    },
    {
        "question": "Which gas do plants absorb from the atmosphere for photosynthesis?",
        "options": ["Oxygen", "Carbon Dioxide", "Nitrogen", "Hydrogen"],
        "answer": "Carbon Dioxide"
    },
    {
        "question": "Which city is known as the 'City of Joy' in India?",
        "options": ["Mumbai", "Chennai", "Kolkata", "Hyderabad"],
        "answer": "Kolkata"
    }
]

# Global variables
question_index = 0
score = 0
selected_answers = []
timer_seconds = 20
timer_id = None

# Function to load the next question
def load_question():
    global question_index, timer_seconds, timer_id
    if question_index < len(questions):
        q = questions[question_index]
        question_label.config(text=q["question"])
        for i in range(4):
            option_buttons[i].config(text=q["options"][i], state="normal")
        timer_seconds = 20
        timer_label.config(text=f"🕒 Time Left: {timer_seconds}s")
        run_timer()
    else:
        show_scoreboard()

# Function to check the selected answer
def check_answer(selected_option):
    global question_index, score, timer_id
    root.after_cancel(timer_id)

    correct_answer = questions[question_index]["answer"]
    selected_answers.append((questions[question_index]["question"], selected_option, correct_answer))

    if selected_option == correct_answer:
        score += 1
    question_index += 1
    load_question()

# Function when time runs out
def time_up():
    global question_index
    selected_answers.append((questions[question_index]["question"], "No Answer", questions[question_index]["answer"]))
    question_index += 1
    load_question()

# Function to run the timer
def run_timer():
    global timer_seconds, timer_id
    timer_label.config(text=f" Time Left: {timer_seconds}s")
    if timer_seconds > 0:
        timer_seconds -= 1
        timer_id = root.after(1000, run_timer)
    else:
        time_up()

# Function to display final scoreboard
def show_scoreboard():
    for widget in root.winfo_children():
        widget.destroy()

    root.configure(bg="#282a36")

    title = tk.Label(root, text=" Quiz Completed!", font=("Helvetica", 26, "bold"),
                     fg="#50fa7b", bg="#282a36")
    title.pack(pady=30)

    total_qs = len(questions)
    correct = score
    wrong = sum(1 for q in selected_answers if q[1] != q[2] and q[1] != "No Answer")
    unanswered = sum(1 for q in selected_answers if q[1] == "No Answer")

    summary = f"Total Questions: {total_qs}\nCorrect Answers: {correct}\nWrong Answers: {wrong}\nUnanswered: {unanswered}"

    summary_label = tk.Label(root, text=summary, font=("Helvetica", 18),
                             fg="#f8f8f2", bg="#282a36", justify="left")
    summary_label.pack(pady=20)

    review_btn = tk.Button(root, text=" Review Answers", font=("Helvetica", 14),
                           bg="#bd93f9", fg="#282a36", width=20, command=show_review)
    review_btn.pack(pady=10)

    play_again_btn = tk.Button(root, text=" Play Again", font=("Helvetica", 14),
                               bg="#50fa7b", fg="#282a36", width=20, command=restart_quiz)
    play_again_btn.pack(pady=10)

    quit_btn = tk.Button(root, text=" Quit", font=("Helvetica", 14),
                         bg="#ff5555", fg="#f8f8f2", width=20, command=root.destroy)
    quit_btn.pack(pady=10)

# Function to display the answer review
def show_review():
    review_message = ""
    for q_text, selected, correct in selected_answers:
        review_message += f"\nQ: {q_text}\nYour Answer: {selected}\nCorrect Answer: {correct}\n"
    messagebox.showinfo("Answer Review ", review_message)

# Function to restart the quiz
def restart_quiz():
    global question_index, score, selected_answers, timer_seconds
    question_index = 0
    score = 0
    selected_answers = []
    timer_seconds = 20
    for widget in root.winfo_children():
        widget.destroy()
    setup_quiz_screen()
    load_question()

# Function to set up the quiz UI
def setup_quiz_screen():
    root.configure(bg="#1e1e2f")

    global question_label, option_buttons, timer_label
    question_label = tk.Label(root, text="", font=("Helvetica", 18, "bold"),
                              bg="#1e1e2f", fg="#f8f8f2", wraplength=550, justify="center")
    question_label.pack(pady=30)

    option_buttons.clear()
    button_colors = ["#6272a4", "#50fa7b", "#ff79c6", "#f1fa8c"]

    for i in range(4):
        btn = tk.Button(root, text="", font=("Helvetica", 14),
                        width=25, fg="#282a36", bg=button_colors[i],
                        activebackground="#bd93f9", activeforeground="white",
                        relief="raised", bd=4,
                        command=lambda i=i: check_answer(option_buttons[i]["text"]))
        btn.pack(pady=8)
        option_buttons.append(btn)

    timer_label = tk.Label(root, text="", font=("Helvetica", 16, "bold"),
                           fg="#ff5555", bg="#1e1e2f")
    timer_label.pack(pady=30)

# GUI setup
root = tk.Tk()
root.title(" Ultimate Quiz Challenge ")
root.geometry("600x600")

option_buttons = []
setup_quiz_screen()
load_question()

root.mainloop()

