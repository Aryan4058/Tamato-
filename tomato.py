import ssl
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import json
import urllib.request
import base64
import io

class Smiley_Game:
    def _init_(self, root):
        self.root = root
        self.root.title("Tomato_game")
        self.root.geometry("800x600+350+100")
        self.root.resizable(False, False)

        self.name = "Aryan"  # Replace with the desired name
        self.score = 0

        self.photo = None  # PhotoImage object

        # label for name
        self.name_label = tk.Label(root, text=f'Name: {self.name}',
                                   font=("Impact", 18, "bold"), bg='blue', fg="white")
        self.name_label.place(x=220, y=10)

        # label for score
        self.score_label = tk.Label(root, text=f'Score: {self.score}',
                                    font=("Impact", 18, "bold"), bg='white', fg="black")
        self.score_label.place(x=220, y=60)

        self.imagelab = tk.Label(root)
        self.imagelab.place(x=70, y=100)

        # Entry Input
        self.answer = tk.Entry(root, font=(
            "times new Roman", 14), bg="lightgray")
        self.answer.place(x=300, y=470, width=200, height=50)

        result = tk.Button(root, text="Submit", cursor="hand2", command=self.result_function,
                          font=("times new Roman", 14), bg="white", fg="black", activebackground="white")
        result.place(x=520, y=470, width=120)

        self.show_image()

    @staticmethod
    def create_image():
        ssl._create_default_https_context = ssl._create_unverified_context
        api_url = "http://marcconrad.com/uob/tomato/api.php"
        response = urllib.request.urlopen(api_url)
        smile_json = json.loads(response.read())
        question = smile_json['question']
        solution = smile_json['solution']
        return question, solution

    def show_image(self):
        self.ques, self.soln = Smiley_Game.create_image()
        with urllib.request.urlopen(self.ques) as u:
            raw_data = u.read()
        image = Image.open(io.BytesIO(raw_data))
        self.photo = ImageTk.PhotoImage(image)

        self.imagelab.config(image=self.photo)
        self.imagelab.image = self.photo  # Keep a reference
        self.imagelab.update()

    def result_function(self):
        if self.answer.get() == "":
            messagebox.showerror("Error", "Please submit the answer", parent=self.root)
        elif self.answer.get() != str(self.soln):
            messagebox.showerror("Error", "Try Again!", parent=self.root)
            self.answer.delete(0, tk.END)
        else:
            messagebox.showinfo("Success", "Correct Answer!", parent=self.root)
            self.score += 1
            self.answer.delete(0, tk.END)
            self.score_label.config(text=f'Score: {self.score}')
            self.show_image()

def main():
    root = tk.Tk()
    img = Smiley_Game(root)
    root.config(bg='blue')
    root.mainloop()

if __name__ == '_main_':
    main()