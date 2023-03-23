from tkinter import filedialog

from keras.models import load_model
from tkinter import *
from PIL import ImageGrab, Image
import numpy as np

model = load_model('mnist.h5')

def predict_digit(img):
    #resize image to 28x28 pixels
    img = img.resize((28,28))
    #convert rgb to grayscale
    img = img.convert('L')
    img = np.array(img)
    #reshaping for model normalization
    img = img.reshape(1,28,28,1)
    img = img/255.0

    #predicting the class
    res = model.predict([img])[0]
    return np.argmax(res), max(res)

class App:
    def __init__(self):
        self.root = Tk()
        self.root.title("Digit Recognizer")
        self.x = self.y = 0
        # Creating elements
        self.canvas = Canvas(self.root, width=300, height=300, bg="white", cursor="cross")
        self.label = Label(self.root, text="Analyzing..", font=("Helvetica", 48))
        self.classify_btn = Button(self.root, text="Searched", command=self.classify_handwriting)
        self.button_clear = Button(self.root, text="Dlt", command=self.clear_all)
        self.button_save = Button(self.root, text="Save", command=self.save_image)
        self.button_save.grid(row=1, column=2, pady=2)

        # Grid structure
        self.canvas.grid(row=0, column=0, pady=2, sticky=W, )
        self.label.grid(row=0, column=1, pady=2, padx=2)
        self.classify_btn.grid(row=1, column=1, pady=2, padx=2)
        self.button_clear.grid(row=1, column=0, pady=2)
        self.canvas.bind("<B1-Motion>", self.draw_lines)

    def save_image(self):
        # Get the image of the canvas
        x = self.root.winfo_rootx() + self.canvas.winfo_x()
        y = self.root.winfo_rooty() + self.canvas.winfo_y()
        x1 = x + self.canvas.winfo_width()
        y1 = y + self.canvas.winfo_height()
        im = ImageGrab.grab((x, y, x1, y1))

        # Ask the user to choose a file name and location
        file_path = filedialog.asksaveasfilename(defaultextension=".png")

        # Save the image
        im.save(file_path)

    def clear_all(self):
        self.canvas.delete("all")

    def classify_handwriting(self):
        # Get the image of the canvas
        x = self.root.winfo_rootx() + self.canvas.winfo_x()
        y = self.root.winfo_rooty() + self.canvas.winfo_y()
        x1 = x + self.canvas.winfo_width()
        y1 = y + self.canvas.winfo_height()
        im = ImageGrab.grab((x, y, x1, y1))

        digit, acc = predict_digit(im)
        self.label.configure(text=str(digit) + ', ' + str(int(acc*100)) + '%')

    def draw_lines(self, event):
        self.x = event.x
        self.y = event.y
        r = 8
        self.canvas.create_oval(self.x - r, self.y - r, self.x + r, self.y + r, fill='black')



    def run(self):
        self.root.mainloop()

app = App()
app.run()
