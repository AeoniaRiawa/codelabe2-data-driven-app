from pathlib import Path
from tkinter import Tk, Canvas, Button, PhotoImage, Frame
import requests
import random
import html

OUTPUT_PATH = Path(__file__).parent

ASSETS_PATH_GUI = OUTPUT_PATH / Path(r"C:\Users\Aeonia\Documents\GitHub\Codelab2 Assessment\build\assets\frame0")
ASSETS_PATH_GUI1 = OUTPUT_PATH / Path(r"C:\Users\Aeonia\Documents\GitHub\Codelab2 Assessment\build\assets\frame1")

def relative_to_assets(path: str, gui="gui") -> Path:
    if gui == "gui":
        return ASSETS_PATH_GUI / Path(path)
    elif gui == "gui1":
        return ASSETS_PATH_GUI1 / Path(path)

def fetch_questions():
    url = "https://opentdb.com/api.php?amount=40&difficulty=hard&type=boolean"
    response = requests.get(url)
    data = response.json()
    #decode HTML entities for each question
    for question in data['results']:
        question['question'] = html.unescape(question['question'])
        question['correct_answer'] = html.unescape(question['correct_answer'])
    return data['results']

class TriviaApp:
    def __init__(self, master):
        self.master = master
        self.questions = fetch_questions()
        self.current_question = None
        self.score = 0

        # Frame for GUI
        self.gui_frame = Frame(master, bg="#FFFFFF")
        self.gui_frame.pack(fill="both", expand=True)

        self.canvas_gui = Canvas(
            self.gui_frame,
            bg="#FFFFFF",
            height=480,
            width=480,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas_gui.place(x=0, y=0)

        self.image_gui_1 = PhotoImage(file=relative_to_assets("image_1.png", gui="gui"))
        self.canvas_gui.create_image(240.0, 240.0, image=self.image_gui_1)

        self.image_gui_2 = PhotoImage(file=relative_to_assets("image_2.png", gui="gui"))
        self.canvas_gui.create_image(240.0, 103.0, image=self.image_gui_2)

        self.button_gui_1 = PhotoImage(file=relative_to_assets("button_1.png", gui="gui"))
        Button(
            self.gui_frame,
            image=self.button_gui_1,
            borderwidth=0,
            highlightthickness=0,
            command=self.switch_to_gui1,
            relief="flat"
        ).place(x=110.0, y=330.0, width=260.4307556152344, height=67.0)

        #frame for GUI1
        self.gui1_frame = Frame(master, bg="#FFFFFF")

        self.canvas_gui1 = Canvas(
            self.gui1_frame,
            bg="#FFFFFF",
            height=480,
            width=480,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas_gui1.place(x=0, y=0)

        self.image_gui1_1 = PhotoImage(file=relative_to_assets("image_1.png", gui="gui1"))
        self.canvas_gui1.create_image(240.0, 240.0, image=self.image_gui1_1)

        self.image_gui1_2 = PhotoImage(file=relative_to_assets("image_2.png", gui="gui1"))
        self.canvas_gui1.create_image(244.0, 132.0, image=self.image_gui1_2)

        self.image_gui1_3 = PhotoImage(file=relative_to_assets("image_3.png", gui="gui1"))
        self.canvas_gui1.create_image(240.0, 398.0, image=self.image_gui1_3)

        self.button_gui1_1 = PhotoImage(file=relative_to_assets("button_1.png", gui="gui1"))
        Button(
            self.gui1_frame,
            image=self.button_gui1_1,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.check_answer("True"),
            relief="flat"
        ).place(x=28.0, y=359.0, width=159.0, height=77.0)

        self.button_gui1_2 = PhotoImage(file=relative_to_assets("button_2.png", gui="gui1"))
        Button(
            self.gui1_frame,
            image=self.button_gui1_2,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.check_answer("False"),
            relief="flat"
        ).place(x=299.0, y=359.0, width=159.0, height=77.0)

        #label for feedback
        self.result_label = self.canvas_gui1.create_text(
            240.0, 250.0,
            text="",
            fill="black",
            font=("Arial", 16, "bold"),
            tags="result_text"
        )

        #score label
        self.score_label = self.canvas_gui1.create_text(
            240.0, 50.0,
            text=f"Score: {self.score}",
            fill="black",
            font=("Arial", 14, "bold"),
            tags="score_text"
        )

        #display the first frame initially
        self.gui_frame.pack(fill="both", expand=True)

    def switch_to_gui1(self):
        """Switch to the second frame (GUI1) and start the trivia game."""
        #after start button is clicked it will hide itself
        self.gui_frame.pack_forget()
        #show the second frame
        self.gui1_frame.pack(fill="both", expand=True)  
        self.next_question()

    def next_question(self):
        """Display the next trivia question."""
        self.current_question = random.choice(self.questions)
        #display the question over image_2
         #remove the previous question
        self.canvas_gui1.delete("question_text")
        self.canvas_gui1.create_text(
            244.0, 132.0,
            text=self.current_question['question'],
            fill="black",
            font=("Arial", 14, "bold"),
            tags="question_text",
            #wrap text within 400 pixels
            width=400
        )

        #clear result label
        self.canvas_gui1.itemconfig(self.result_label, text="")

    def check_answer(self, answer):
        """Check the user's answer and provide feedback."""
        correct_answer = self.current_question['correct_answer']
        if answer == correct_answer:
            self.canvas_gui1.itemconfig(self.result_label, text="Correct!", fill="green")
            self.score += 1  # adds score
        else:
            self.canvas_gui1.itemconfig(self.result_label, text="Wrong!", fill="red")

        #score label
        self.canvas_gui1.itemconfig(self.score_label, text=f"Score: {self.score}")
        
        #proceed to the next question after 0.5
        self.master.after(500, self.next_question)
if __name__ == "__main__":
    window = Tk()
    window.geometry("480x480")
    window.configure(bg="#FFFFFF")
    window.resizable(False, False)
    app = TriviaApp(window)
    window.mainloop()
