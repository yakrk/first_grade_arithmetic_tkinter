import tkinter as tk
from tkinter import ttk
import random
from PIL import Image, ImageTk
from image_path import *

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
is_game_on = True

# Level Settings
SECONDS = 60
ARITHMATIC_CHOICE = ["+","-"]
MIN_NUM = 10
MAX_NUMM = 40
MAX_LIFE = 10
remaining_life = MAX_LIFE
life_list = []

# Prep Images
start_image = tk.PhotoImage(file = start_image_path)
correct_image = tk.PhotoImage(file = correct_image_path)
boo_image = tk.PhotoImage(file = boo_image_path)
gameover_image = tk.PhotoImage(file = gameover_image_path)
ball_image = tk.PhotoImage(file = ball_image_path)
start_resized_image = start_image.subsample(6, 6)
correct_resized_image = correct_image.subsample(6, 6)
boo_resized_image = boo_image.subsample(6, 6)
gameover_resized_image = gameover_image.subsample(2,2)
ball_resized_image = ball_image.subsample(20,20)

#Timer class
class Timer:
    def __init__(self):
        self.count = SECONDS
        self.count_down()
        self.timer = None

    def count_down(self):
        global entered_text
        remaining_time.config(text=f"のこりじかん: {self.count} びょう")
        if self.count > 0:
            self.count -= 1
            self.timer = window.after(1000, self.count_down)
        else:
            game_over()
        window.update()

    def reset_countdown(self):
        window.after_cancel(self.timer)
        self.count = SECONDS
        self.count_down()

# Create question class
class Question:
    def __init__(self) -> None:
        self.min = MIN_NUM
        self.max = MAX_NUMM
        self.first_num = None
        self.second_num = None
        self.arithmatics = ARITHMATIC_CHOICE
        self.arithmatic = None
        self.create_question()
        
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


def show_question():
    global question
    question = Question()

def game_over():
    global is_game_on
    restart_btn.place(x=150,y=150)
    background_image.config(image=gameover_resized_image)
    remaining_time.config(text="ゲームオーバー！！")
    is_game_on = False
    text_entry.place_forget()

def restart():
    global is_game_on
    global score
    text_entry.delete("1.0","end")
    text_entry.place(x=10,y=120)
    score = 0
    is_game_on = True
    reset_life()
    score_label.config(text = f"Score: {score}")
    background_image.config(image=start_resized_image)
    countdown.reset_countdown()
    restart_btn.place_forget()

def reset_life():
    global remaining_life
    remaining_life = MAX_LIFE
    for i in range(remaining_life):
        xcor = 10 + 30*i
        i = tk.Label(image=ball_resized_image, background=BACKGROUND_COLOR)
        i.place(x=xcor, y=45)
        life_list.append(i)
    
def type_event(event):
    global score
    global life_list
    global is_game_on
    if is_game_on:
        result=text_entry.get(1.0, tk.END+"-1c")
        answer = question.get_answer()
        # if correct
        if int(result) == answer:
            countdown.reset_countdown()
            score += 1
            score_label.config(text = f"Score: {score}")
            background_image.config(image=correct_resized_image)
            show_question()
        # if wrong
        else:
            if len(life_list)<1:
                game_over()
            else:
                for i, value in enumerate(life_list):
                    if i == len(life_list)-1:
                        value.destroy()
                del life_list[-1]
                background_image.config(image=boo_resized_image)
        text_entry.delete("1.0","end")


# Show score
score_label = tk.Label(text="Score: 0", background=BACKGROUND_COLOR, font=("Arial", 12))

# Create remaining time label
remaining_time = tk.Label(
    text="", background=BACKGROUND_COLOR, font=("Arial", 12))
# Show entered text
question_label = tk.Label(text="もんだい", background=BACKGROUND_COLOR, anchor="w",
                      width=400, wraplength=700, justify="left", font=("Arial", 18), foreground="#000000")
text_entry = tk.Text(width=20, height=2, background=BACKGROUND_COLOR, font=("Arial", 20))
restart_btn = tk.Button(command=restart, text="スタート")
# Create a photoimage object of the image in the path
background_image = tk.Label(image=start_resized_image, background=BACKGROUND_COLOR)

# Place images
score_label.place(x=150, y=0)
remaining_time.place(x=100,y=20)
question_label.place(x=10,y=80)
text_entry.place(x=10,y=120)
background_image.place(x=50,y=200)

# catch press Enter key 
event_sequence = '<Return>'
window.bind(event_sequence, type_event)

#start upon launch
countdown = Timer()
reset_life()
show_question()


window.mainloop()
