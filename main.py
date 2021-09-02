import tkinter as tk
from tkinter import messagebox
import pandas as pd
from random import choice
import os

BACKGROUND_COLOR = "#B1DDC6"
SMALL_FONT = ("Arial", 40, "italic")
BOLD_FONT = ("Arial", 40, "bold")
LANGUAGE_CSV = "data/french_words.csv"
WORDS_TO_LEARN = "data/words_to_learn.csv"

# --- Pandas component ---
try:
    data = pd.read_csv(WORDS_TO_LEARN)
except FileNotFoundError:
    data = pd.read_csv(LANGUAGE_CSV)
finally:
    to_learn = data.to_dict(orient="records")
current_card = {}


def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    canvas.itemconfig(card, image=card_front)
    # load_random = data["French"].sample(replace=True).to_string(index=False)
    current_card = choice(to_learn)
    load_language = data.columns[0]
    language.config(text=load_language, bg="#FFFFFF", fg="black")
    word.config(text=current_card["French"], bg="#FFFFFF", fg="black")
    flip_timer = window.after(ms=3000, func=flipper)


def flipper():
    canvas.itemconfig(card, image=card_back)
    english = data.columns[1]
    # translation = data.loc[data.French == word.cget("text")].values[0][1]
    translation = current_card["English"]
    language.config(text=english, bg="#91C2AF", fg="white")
    word.config(text=translation, bg="#91C2AF", fg="white")


def guess_right():
    to_learn.remove(current_card)
    if to_learn != []:
        pd.DataFrame(to_learn).to_csv(WORDS_TO_LEARN, index=False)
        next_card()
    else:
        os.remove(WORDS_TO_LEARN)
        messagebox.showinfo(title="Done!", message="No more words to learn!")
        os.sys.exit()


# --- UI component ---

window = tk.Tk()
window.title("Flashcard App")
window.config(bg="#B1DDC6", padx=50, pady=50)
window.resizable(False, False)

flip_timer = window.after(3000, func=flipper)


canvas = tk.Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_back = tk.PhotoImage(file="images/card_back.png")
card_front = tk.PhotoImage(file="images/card_front.png")
# canvas.create_image(800, 526, image=card_back)
card = canvas.create_image(400, 263, image=card_front)
language = tk.Label(text="", font=SMALL_FONT, bg="#FFFFFF")
language.place(x=400, y=150, anchor="n")
word = tk.Label(text="", font=BOLD_FONT, bg="#FFFFFF")
word.place(x=400, y=263, anchor="n")
next_card()
canvas.grid(column=0, row=0, columnspan=2)

right = tk.PhotoImage(file="images/right.png")
r_button = tk.Button(
    image=right,
    highlightthickness=0,
    bg=BACKGROUND_COLOR,
    borderwidth=0,
    command=guess_right,
)
r_button.grid(column=0, row=1)

wrong = tk.PhotoImage(file="images/wrong.png")
w_button = tk.Button(
    image=wrong,
    highlightthickness=0,
    bg=BACKGROUND_COLOR,
    borderwidth=0,
    command=next_card,
)
w_button.grid(column=1, row=1)


window.mainloop()
