import subprocess as sb_p
import tkinter as tk
import registerVoter as regV
import admFunc as adFunc
from tkinter import *
from registerVoter import *
from admFunc import *
from PIL import Image, ImageTk

def AdminHome(root, frame1, frame3):
    root.title("Admin")
    for widget in frame1.winfo_children():
        widget.destroy()

    # Set background image
    try:
        bg_image = Image.open("img/bg.png")
        bg_image = bg_image.resize((root.winfo_screenwidth(), root.winfo_screenheight()), Image.Resampling.LANCZOS)
        bg_photo = ImageTk.PhotoImage(bg_image)
        bg_label = Label(frame1, image=bg_photo)
        bg_label.image = bg_photo
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    except Exception as e:
        print(f"Background image error in AdminHome: {e}")
        frame1.config(bg='lightblue')

    # Remove frame3
    if frame3 and frame3.winfo_ismapped():
        frame3.pack_forget()

    # Calculate positions for laptop DISPLAY area
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    laptop_center_x = screen_width // 2
    laptop_center_y = screen_height // 2 - 100

    # HOME and ADMIN BUTTONS (reduced size)
    home_btn = Button(frame1, text="🏠 Home", font=('Helvetica', 12, 'bold'), 
                     command=lambda: __import__('homePage').Home(root, frame1, Frame(root)),
                     bg='lightblue', fg='black', relief='raised', bd=2, 
                     width=10, height=1, cursor='hand2')
    home_btn.place(x=20, y=20)

    admin_btn = Button(frame1, text="👨‍💼 Admin", font=('Helvetica', 12, 'bold'), 
                      command=lambda: AdminHome(root, frame1, frame3),
                      bg='lightgreen', fg='black', relief='raised', bd=2, 
                      width=10, height=1, cursor='hand2')
    admin_btn.place(x=140, y=20)

    # Title positioned at top of laptop DISPLAY
    title_label = Label(frame1, text="Admin Dashboard", font=('Helvetica', 30, 'bold'), 
                       bg='black', fg='white', bd=0)
    title_label.place(x=laptop_center_x, y=laptop_center_y - 150, anchor='center')

    # Buttons positioned inside laptop DISPLAY (reduced size, removed Reset)
    button_y_start = laptop_center_y - 50
    button_spacing = 70

    runServer = Button(frame1, text="Run Server", width=15, height=1, font=('Helvetica', 16, 'bold'),
                      command=lambda: sb_p.call('start python Server.py', shell=True),
                      bg='#4CAF50', fg='white', relief='raised', bd=3, cursor='hand2')
    runServer.place(x=laptop_center_x, y=button_y_start, anchor='center')

    registerVoter = Button(frame1, text="Register Voter", width=15, height=1, font=('Helvetica', 16, 'bold'),
                          command=lambda: regV.registerVoter(root, frame1),
                          bg='#2196F3', fg='white', relief='raised', bd=3, cursor='hand2')
    registerVoter.place(x=laptop_center_x, y=button_y_start + button_spacing, anchor='center')

    showVotes = Button(frame1, text="Show Votes", width=15, height=1, font=('Helvetica', 16, 'bold'),
                      command=lambda: adFunc.showVotes(root, frame1),
                      bg='#FF9800', fg='white', relief='raised', bd=3, cursor='hand2')
    showVotes.place(x=laptop_center_x, y=button_y_start + button_spacing*2, anchor='center')

    frame1.pack(fill=BOTH, expand=True)
    # REMOVED: root.mainloop() - This was causing the infinite loop

def log_admin(root, frame1, admin_ID, password):
    if admin_ID == "Admin" and password == "admin":
        frame3 = Frame(root)
        AdminHome(root, frame1, frame3)
    else:
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        laptop_center_x = screen_width // 2
        laptop_center_y = screen_height // 2 - 100
        
        # Remove any existing error messages first
        for widget in frame1.winfo_children():
            if isinstance(widget, Label) and "Incorrect" in widget.cget('text'):
                widget.destroy()
        
        msg = Label(frame1, text="Either ID or Password is Incorrect", font=('Helvetica', 14, 'bold'), 
                   bg='black', fg='red')
        msg.place(x=laptop_center_x, y=laptop_center_y + 120, anchor='center')
        
        # Auto remove error message after 3 seconds
        frame1.after(3000, msg.destroy)

def AdmLogin(root, frame1):
    root.title("Admin Login")
    for widget in frame1.winfo_children():
        widget.destroy()

    # Set background image
    try:
        bg_image = Image.open("img/bg.png")
        bg_image = bg_image.resize((root.winfo_screenwidth(), root.winfo_screenheight()), Image.Resampling.LANCZOS)
        bg_photo = ImageTk.PhotoImage(bg_image)
        bg_label = Label(frame1, image=bg_photo)
        bg_label.image = bg_photo
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    except Exception as e:
        print(f"Background image error in AdmLogin: {e}")
        frame1.config(bg='lightblue')

    # Calculate positions for laptop DISPLAY area
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    laptop_center_x = screen_width // 2
    laptop_center_y = screen_height // 2 - 100

    # HOME BUTTON (reduced size)
    home_btn = Button(frame1, text="🏠 Home", font=('Helvetica', 12, 'bold'), 
                     command=lambda: __import__('homePage').Home(root, frame1, Frame(root)),
                     bg='lightblue', fg='black', relief='raised', bd=2, 
                     width=10, height=1, cursor='hand2')
    home_btn.place(x=20, y=20)

    # Title positioned at top of laptop DISPLAY
    title_label = Label(frame1, text="Admin Login", font=('Helvetica', 30, 'bold'), 
                       bg='black', fg='white', bd=0)
    title_label.place(x=laptop_center_x, y=laptop_center_y - 100, anchor='center')

    # Form positioned inside laptop DISPLAY
    form_start_y = laptop_center_y - 20
    label_x = laptop_center_x - 100
    entry_x = laptop_center_x + 50
    spacing = 60

    # Labels and entries
    Label(frame1, text="Admin ID:", font=('Helvetica', 16, 'bold'), bg='black', fg='white').place(x=label_x, y=form_start_y, anchor='e')
    Label(frame1, text="Password:", font=('Helvetica', 16, 'bold'), bg='black', fg='white').place(x=label_x, y=form_start_y + spacing, anchor='e')

    admin_ID = tk.StringVar()
    password = tk.StringVar()

    e1 = Entry(frame1, textvariable=admin_ID, font=('Helvetica', 14), width=18, bd=2, relief='sunken')
    e1.place(x=entry_x, y=form_start_y, anchor='center')
    
    e2 = Entry(frame1, textvariable=password, show='*', font=('Helvetica', 14), width=18, bd=2, relief='sunken')
    e2.place(x=entry_x, y=form_start_y + spacing, anchor='center')

    def perform_login():
        log_admin(root, frame1, admin_ID.get(), password.get())

    # Login button (reduced size)
    sub = Button(frame1, text="Login", width=12, height=1, font=('Helvetica', 16, 'bold'),
                command=perform_login, bg='#4CAF50', fg='white', relief='raised', bd=3, cursor='hand2')
    sub.place(x=laptop_center_x, y=form_start_y + spacing*2, anchor='center')

    # Fixed Enter key binding
    def on_enter(event):
        perform_login()

    root.bind('<Return>', on_enter)
    e1.bind('<Return>', on_enter)
    e2.bind('<Return>', on_enter)

    frame1.pack(fill=BOTH, expand=True)
    # REMOVED: root.mainloop() - This was causing the infinite loop

# if __name__ == "__main__":
#     root = Tk()
#     root.geometry('500x500')
#     frame1 = Frame(root)
#     frame3 = Frame(root)
#     AdminHome(root, frame1, frame3)