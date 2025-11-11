import subprocess as sb_p
import tkinter as tk
from tkinter import *
from Admin import AdmLogin
from voter import voterLogin
from PIL import Image, ImageTk

def Home(root, frame1, frame2):
    for frame in root.winfo_children():
        for widget in frame.winfo_children():
            widget.destroy()

    # Set background image using PIL for PNG support
    try:
        bg_image = Image.open("img/bg.png")
        bg_image = bg_image.resize((root.winfo_screenwidth(), root.winfo_screenheight()), Image.Resampling.LANCZOS)
        bg_photo = ImageTk.PhotoImage(bg_image)
        bg_label = Label(frame1, image=bg_photo)
        bg_label.image = bg_photo
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    except Exception as e:
        print(f"Background image error: {e}")
        frame1.config(bg='lightgray')

    # Remove frame2 (navigation bar)
    frame2.pack_forget()

    # Calculate positions for laptop DISPLAY area
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    laptop_center_x = screen_width // 2
    laptop_center_y = screen_height // 2 - 100

    # Home button at top left
    home_btn = Button(frame1, text="🏠 Home", font=('Helvetica', 12, 'bold'), 
                     command=lambda: Home(root, frame1, frame2),
                     bg='lightblue', fg='black', relief='raised', bd=2, 
                     width=10, height=1, cursor='hand2')
    home_btn.place(x=20, y=20)

    root.title("Home")

    # Title positioned at top of laptop DISPLAY
    title_label = Label(frame1, text="Online Voting System", font=('Helvetica', 30, 'bold'), 
                       bg='black', fg='white', bd=0)
    title_label.place(x=laptop_center_x, y=laptop_center_y - 120, anchor='center')
    
    # Buttons positioned inside laptop DISPLAY (reduced size)
    button_y_start = laptop_center_y - 30
    button_spacing = 70

    admin = Button(frame1, text="Admin Login", width=15, height=1, font=('Helvetica', 16, 'bold'),
                  command=lambda: AdmLogin(root, frame1), bg='#4CAF50', fg='white',
                  relief='raised', bd=3, cursor='hand2')
    admin.place(x=laptop_center_x, y=button_y_start, anchor='center')

    voter = Button(frame1, text="Voter Login", width=15, height=1, font=('Helvetica', 16, 'bold'),
                  command=lambda: voterLogin(root, frame1), bg='#2196F3', fg='white',
                  relief='raised', bd=3, cursor='hand2')
    voter.place(x=laptop_center_x, y=button_y_start + button_spacing, anchor='center')

    newTab = Button(frame1, text="New Window", width=15, height=1, font=('Helvetica', 16, 'bold'),
                   command=lambda: sb_p.call('start python homePage.py', shell=True), 
                   bg='#FF9800', fg='white', relief='raised', bd=3, cursor='hand2')
    newTab.place(x=laptop_center_x, y=button_y_start + button_spacing*2, anchor='center')

    frame1.pack(fill=BOTH, expand=True)
    root.mainloop()

def new_home():
    root = Tk()
    root.attributes('-fullscreen', True)
    root.bind('<Escape>', lambda e: root.attributes('-fullscreen', False))
    
    frame1 = Frame(root)
    frame2 = Frame(root)
    Home(root, frame1, frame2)

if __name__ == "__main__":
    new_home()