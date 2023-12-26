from tkinter import filedialog, Tk, Button, Label, Canvas, messagebox
from PIL import Image, ImageTk
from rembg import remove
import os
from tkinter import ttk
from ttkthemes import ThemedTk
from tkinter import PhotoImage
class Application:
    def __init__(self, master=None):
        self.master = master
        self.master.title("Background Remover")
        self.master.geometry("800x600")
        self.background_img = ImageTk.PhotoImage(Image.open('bg.jpg'))  # Carrega img de fundo
        self.background_label = Label(self.master, image=self.background_img)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)  # Set the background image
        #self.master.configure(bg='/bg.jpg')  # custom background
        self.input_path = None
        self.output_path = None
        self.title = Label(self.master, text="Background Remover", fg='grey', font=("Helvetica", 50))  # Title
        self.title.pack(pady=20)
        self.process = ttk.Button(self.master, text="Start", command=self.process_image)
        self.process.pack(pady=20)
        self.imgFrame = ttk.Frame(self.master)  # Frame to hold the images
        self.imgFrame.pack(pady=20)
        self.imgLabel = Label(self.imgFrame)
        self.resultLabel = Label(self.imgFrame)
        self.resultText = Label(self.master, text="The background was removed", fg='grey', font=("Helvetica", 30))  # Result text
        self.resultText.pack(pady=50)  # Increase the space between the text and the button
        self.resultText.pack_forget()  # Hide the text initially
        self.viewPath = ttk.Button(self.master, text="Open Image Path", command=self.open_image_location) # Button to open the image location
        self.viewPath.pack(pady=20)  # Hide the button initially
        self.viewPath.pack_forget()  # Hide the button initially

    def select_input_file(self):
        self.input_path = filedialog.askopenfilename(title="Select a file", filetypes=[("Image files", "*.jpg *.jpeg *.png")])
        if not self.input_path:
            messagebox.showerror("Error", "No image selected.")
            return False
        self.show_img(self.input_path, self.imgLabel)  # Show the loaded image
        return True

    def select_output_file(self):
        self.output_path = filedialog.asksaveasfilename(title="Save file as...")
        if not self.output_path.endswith('.png'):
            self.output_path += '.png'

    def process_image(self):
        if not self.select_input_file():
            return
        self.select_output_file()
        try:
            input_img = Image.open(self.input_path)  # Corrected
            output = remove(input_img)
            output.save(self.output_path)
            self.show_img(self.output_path, self.resultLabel)  # Show the result
            self.resultText.pack()  # Show the text after the image is processed
            self.viewPath.pack()  # Show the button after the image is processed
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def show_img(self, imagePath, label):
        image = Image.open(imagePath)
        max_size = (400, 400)
        image.thumbnail(max_size)
        photo = ImageTk.PhotoImage(image)
        label.config(image=photo)
        label.image = photo
        label.pack(side="left", padx=10, pady=10)  # Position the image on the left with padding

    def open_image_location(self):
        if self.output_path:
            os.system(f'open -R {os.path.realpath(self.output_path)}')

def main():
    root = ThemedTk(theme="equilux")  # Use the "equilux" theme
    root.state('zoomed')  # Start in full screen
    root.minsize(900, 750)  # Minimum window size
    Application(root)
    root.mainloop()

if __name__ == "__main__":
    main()
