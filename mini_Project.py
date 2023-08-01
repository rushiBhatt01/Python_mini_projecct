import tkinter as tk
import random
from PIL import Image, ImageTk
from tkinter import ttk

import time

class TypingSpeedTest(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Typing Speed Test")
        self.current_mode = "Easy"
        self.current_text = ""
        self.current_text_index = 0 
        self.start = 0
        self.duration = 0  
        self.running = False
        self.create_border()
        self.create_widgets()
        
    def create_border(frame, border_width=4, border_color="Black"):
        frame.config(borderwidth=border_width, relief=tk.SOLID, bd=70)
        frame.config(highlightbackground=border_color, highlightcolor=border_color)

    def create_widgets(self):

        main_frame = tk.Frame(self, borderwidth=50, relief=tk.SUNKEN,bg="Dodger Blue")
        main_frame.pack()
        image = Image.open("assets/bg2.png")


        bg_image = ImageTk.PhotoImage(image)


        background_label = tk.Label(main_frame, image=bg_image,font=("Times New Roman", 14))
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
        
        self.timer_label = tk.Label(main_frame, text="Time: 0 s",bg="#3B3B3B", fg="#fff")
        self.timer_label.pack(pady=5)

        self.timer_canvas = tk.Canvas(main_frame, width=100, height=100, bg="black", highlightthickness=0)
        self.timer_canvas.pack(pady=5)
        
        self.info_label = tk.Label(main_frame, text="Select Difficulty Mode:",bg="#3B3B3B", fg="#fff",font=("Times New Roman", 14))
        self.info_label.pack(pady=5)


        self.difficulty_var = tk.StringVar()
        self.difficulty_var.set("Easy")
    

        self.difficulty_options = ["Easy", "Medium", "Hard"]
        self.difficulty_menu = tk.OptionMenu(main_frame, self.difficulty_var, *self.difficulty_options)
        self.difficulty_menu.pack(pady=5)

        self.text_label = tk.Label(main_frame, text="",bg="#3B3B3B", fg="#fff")
        self.text_label.pack(pady=10)

        self.entry = tk.Entry(main_frame,width=130,bg="#E6E6FA", fg="#000000",state=tk.DISABLED,font=("Times New Roman", 14))
        self.entry.pack(pady=5)
       

        self.entry.bind("<Return>", self.submit_test)

        self.slider_label = tk.Label(main_frame, text="Set Timer Duration (in seconds):",bg="#3B3B3B", fg="#fff",font=("Times New Roman", 14))
        self.slider_label.pack(pady=5)


        slider_frame = tk.Frame(main_frame,bg="#3B3B3B",borderwidth=2, relief=tk.SUNKEN)
        slider_frame.pack(pady=5)

        self.timer_slider = ttk.Scale(slider_frame, from_=10, to=120, length=280, orient=tk.HORIZONTAL, command=self.update_slider_label, style="Custom.Horizontal.TScale")
        self.timer_slider.set(60)  # Set the default duration to 60 seconds
        self.timer_slider.pack(padx=2, pady=2)

        self.slider_value_label = tk.Label(main_frame, text=f"Timer: {int(self.timer_slider.get())} seconds",   bg="#3B3B3B", fg="#fff",font=("Times New Roman", 10))
        self.slider_value_label.pack(pady=5)

        
        self.start_button = tk.Button(main_frame, text="Start Test",bg="#3B3B3B", fg="#fff",padx=10, pady=5, command=self.start_test,font=("Times New Roman", 12))
        self.start_button.pack()

        self.result_label = tk.Label(main_frame, text="",bg="#3B3B3B",fg="#fff",padx=10, pady=5,font=("Times New Roman", 14))
        self.result_label.pack()

        self.timer_progress = ttk.Progressbar(main_frame, orient="horizontal", length=800, mode="indeterminate")
        self.timer_progress.pack(pady=5)

        self.timer_running = False


    def animate_text(self):
        if self.current_text_index < len(self.current_text):
            char = self.current_text[self.current_text_index]
            self.current_text_index += 1
            self.text_label.config(text=self.current_text[:self.current_text_index])
            self.after(100, self.animate_text)
        else:
            self.current_text_index = 0


    def generate_text(self, difficulty):
        easy_text = [
            "The sun is shining brightly in the blue sky.",
            "Where there is a will, there is a way.",
            "In the middle of difficulty lies opportunity.",
            "The cat curled up on the cozy couch.",
            "The smell of freshly baked bread filled the air."
        ]
        
        medium_text = [
            "Pack my box with five dozen liquor jugs.",
            "The quick brown fox jumps over the lazy dog.",
            "Reading a good book is a wonderful escape.",
            "The labyrinthine maze challenged even the most adept navigators."
        ]
        
        hard_text = [
            "How razorback jumping frogs can level six piqued gymnasts.",
            "Life is 10% what happens to you and 90 how you react to it.",
            "In the midst of chaos, find the calm; within uncertainty, seek clarity.",
            "A cacophony of thoughts echoed through the corridors of his restless mind.",
            "Amidst the thorns of adversity blooms the flower of triumph.",
            "The audacious mountaineer scaled the vertiginous peaks with unwavering determination."
        ]
       

        if difficulty == "Easy":
            
            self.random_string = random.choice(easy_text)
            return self.random_string
        elif difficulty == "Medium":
            self.random_string = random.choice(medium_text)
            
            return self.random_string
        elif difficulty == "Hard":
            
            self.random_string = random.choice(hard_text)
            return self.random_string
     
    
    def update_slider_label(self, event=None):
       
      self.slider_value_label.config(text=f"Timer: {int(self.timer_slider.get())} seconds")


    def get_timer_duration(self):
        user_input = self.timer_slider.get()
        self.duration = int(user_input) * 1000

   
    

    def start_test(self):
        
        if not self.running:
            self.current_mode = self.difficulty_var.get()
            self.current_text = self.generate_text(self.current_mode)
            self.text_label.config(text=self.current_text)

            self.get_timer_duration()  
            if self.duration <= 0:
               
                self.duration = 60000 

            self.entry.config(state=tk.NORMAL)
            self.entry.delete(0, tk.END)

            self.start = time.time()
            self.running = True
            self.timer_running = True
            self.update_timer()

            self.text_label.config(text="")
            self.current_text_index = 0
            self.animate_text()


    def update_timer(self):
     
       
         if self.timer_running:
            time_elapsed = int(time.time() - self.start)
            time_remaining = max(self.duration - time_elapsed * 1000, 0)  # Convert to milliseconds

            if time_remaining > 0:
                self.timer_label.config(text=f"Time: {time_remaining // 1000} s")
                self.timer_progress["maximum"] = self.duration
                self.timer_progress["value"] = time_elapsed * 1000
                self.update_circle_timer(time_remaining)
                self.timer_label.after(100, self.update_timer)
            else:
                self.timer_label.config(text="Time's up!")
                self.timer_progress["value"] = self.duration
                self.timer_running = False
                self.entry.config(state=tk.DISABLED)

                if self.running:
                    self.running = False
                    self.calculate_accuracy()
         else:
            
            self.update_circle_timer(0)

    def update_circle_timer(self, time_remaining):
        angle = 360 - (360 * time_remaining / self.duration)
        self.timer_canvas.delete("progress_arc")
        self.timer_canvas.create_arc(10, 10, 90, 90, start=90, extent=-angle, style=tk.ARC,
                                     outline="blue", width=6, tags="progress_arc")

    def submit_test(self, event):
       
            self.timer_running = False
            self.entry.config(state=tk.NORMAL)
            self.calculate_accuracy()
            self.after(5000, self.restart_test)
    def calculate_accuracy(self):
        user_input = self.entry.get()
        accuracy = self.compare_text(user_input, self.current_text)
        self.result_label.config(text=f"Accuracy: {accuracy:.2f}%")

        if not self.timer_running:
            words_typed = len(user_input.split())
            minutes_elapsed = (time.time() - self.start) / 60
            wpm = words_typed // minutes_elapsed
            if accuracy>75:
                self.result_label.config(text=f"Accuracy: {accuracy:.2f}% | WPM: {wpm}")
            else:
                self.result_label.config(text=f"Accuracy: {accuracy:.2f}%")
        self.start = 0

        self.start = 0

    def compare_text(self, user_input, original_text):
        original_words = original_text.split()
        user_words = user_input.split()

        correct_words = 0
        for user_word, original_word in zip(user_words, original_words):
            if user_word == original_word:
                correct_words += 1

        accuracy = (correct_words / len(original_words)) * 100
        return accuracy
    def restart_test(self):
       
        self.current_text = ""
        self.current_text_index = 0
        self.text_label.config(text="")
        self.entry.delete(0, tk.END)
        self.result_label.config(text="")
        self.timer_label.config(text="Time: 0 s")
        self.timer_progress["value"] = 0
        self.timer_running = False
        self.running = False
        self.start = 0
        
game=TypingSpeedTest()
game.mainloop()