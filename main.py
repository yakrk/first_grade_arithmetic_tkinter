import tkinter as tk
from tkinter import ttk
import random

# Create a view with Tkinter
BACKGROUND_COLOR = "white"
window = tk.Tk()
window.title("さんすうもんだい")
window.config(padx=20, pady=20, bg=BACKGROUND_COLOR)
window.geometry("400x400")
set_font = 'C:\Windows\Fonts\Arial.ttf'
entered_text = ""
question = None
score = 0

# Level Settings
seconds = 60
arithmatic_choice = ["+","-"]
min_num = 10
max_num = 40

#Timer class
class Timer:
    def __init__(self):
        self.count = seconds
        self.count_down()
        self.timer = None

    def count_down(self):
        global entered_text
        remaining_time.config(text=f"のこりじかん: {self.count} びょう")
        if self.count > 0:
            self.count -= 1
            self.timer = window.after(1000, self.count_down)
        else:
            remaining_time.config(text="ゲームオーバー！！")
            text_entry.pack_forget()
            restart_btn.pack()
        window.update()

    def reset_countdown(self):
        window.after_cancel(self.timer)
        self.count = seconds
        self.count_down()

# Create question class
class Question:
    def __init__(self) -> None:
        self.min = min_num
        self.max = max_num
        self.first_num = None
        self.second_num = None
        self.arithmatics = arithmatic_choice
        self.arithmatic = None
        
    def create_question(self):
        self.first_num = random.randint(self.min, self.max)
        self.second_num = random.randint(self.min, self.max)
        self.arithmatic = random.choice(self.arithmatics)
        if self.first_num < self.second_num:
            question = f"{self.second_num} {self.arithmatic} {self.first_num} ="
        else:
            question = f"{self.first_num} {self.arithmatic} {self.second_num} ="
        question_label.config(text=question)
        window.update()
        
    def get_answer(self):
        if self.arithmatic == "+":
            answer = self.first_num + self.second_num
        else:
            if self.first_num < self.second_num:
                answer = self.second_num - self.first_num
            else: 
                answer = self.first_num - self.second_num
        return answer

def restart():
    global score
    text_entry.pack()
    score = 0
    score_label.config(text = f"Score: {score}")
    countdown.reset_countdown()
    restart_btn.pack_forget()
    main()
    
def type_event(event):
    global score
    result=text_entry.get(1.0, tk.END+"-1c")
    answer = question.get_answer()
    if result == "":
        pass
    elif int(result) == answer:
        countdown.reset_countdown()
        text_entry.delete("1.0","end")
        score += 1
        score_label.config(text = f"Score: {score}")
        main()

# Show score
score_label = tk.Label(text="Score: 0", background=BACKGROUND_COLOR, font=("Arial", 12))
score_label.pack()

# Create remaining time label
remaining_time = tk.Label(
    text="", background=BACKGROUND_COLOR, font=("Arial", 12))
remaining_time.pack()

# Show entered text
question_label = tk.Label(text="もんだい", background=BACKGROUND_COLOR, anchor="w",
                      width=400, wraplength=700, justify="left", font=("Arial", 18), foreground="#000000")
question_label.pack()
text_entry = tk.Text(width=400, height=2, background=BACKGROUND_COLOR, font=("Arial", 20))
text_entry.pack()
restart_btn = tk.Button(command=restart, text="リスタート")

def main():
    global question
    question = Question()
    question.create_question()

event_sequence = '<KeyPress>'
window.bind(event_sequence, type_event)

countdown = Timer()
main()

window.mainloop()
